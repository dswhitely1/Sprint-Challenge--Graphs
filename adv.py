from ast import literal_eval

from player import Player
from util import Queue
from world import World

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}


class Graph:
    def __init__(self):
        self.verticies = {}

    def add(self, room_id, direction):
        if room_id not in self.verticies:
            self.verticies[room_id] = {}
        self.verticies[room_id][direction] = '?'

    def add_edge(self, r1, r2, direction):
        self.verticies[r1][direction] = r2
        self.verticies[r2][reverse_dirs[direction]] = r1

    def get_neighbors(self, room_id):
        ret_list = []
        for key, value in self.verticies[room_id].items():
            if value != '?':
                ret_list.append((key, value))
        return ret_list

    def get_path(self, start, target, path=None, visited=None):
        if path is None:
            path = []
        if visited is None:
            visited = set()
        path = path + [start]
        if start in target:
            return path
        if start not in visited:
            visited.add(start)
            for child in self.get_neighbors(start):
                new_path = self.get_path(child[1], target, path, visited)
                if new_path:
                    return new_path
        return None


class Traversal:
    def __init__(self, robot):
        self.player = robot
        self.maze_graph = Graph()
        self.finished = set()
        self.available_rooms = []
        self.reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        self.directions = {}

    def check_exits(self, room_id):
        for exits in self.maze_graph.verticies[room_id]:
            if self.maze_graph.verticies[room_id][exits] == '?':
                if room_id not in self.available_rooms:
                    self.available_rooms.append(room_id)
                return False
        self.finished.add(room_id)
        if room_id in self.available_rooms:
            self.available_rooms.remove(room_id)
        return True

    def get_next_direction(self, room_id):
        for direction in self.directions:
            if direction in self.maze_graph.verticies[room_id]:
                if self.maze_graph.verticies[room_id][direction] == '?':
                    return direction
        return None

    def retreat(self, room_id):
        if len(self.available_rooms) == 0:
            return None
        # target = self.available_rooms[-1] if len(self.available_rooms) != 1 else self.available_rooms[0]
        target = self.available_rooms
        new_path = self.maze_graph.get_path(room_id, target)
        # print(f'Current Room: {room_id}, Path to next available room: {new_path}')
        return new_path

    def create_room_in_graph(self, r_id, r_exits):
        for r_exit in r_exits:
            self.maze_graph.add(r_id, r_exit)

    def advance(self):
        room_id = self.player.current_room.id
        room_exits = self.player.current_room.get_exits()

        if room_id not in self.maze_graph.verticies:
            self.create_room_in_graph(room_id, room_exits)

        if room_id not in self.finished and self.check_exits(room_id):
            self.finished.add(room_id)

        # Push Available Directions into The Stack

        next_dir = self.get_next_direction(room_id)
        if next_dir is not None:
            self.player.travel(next_dir)
            traversal_path.append(next_dir)
            next_room_id = self.player.current_room.id
            print(f'Advancing to Room {next_room_id}')
            next_room_exits = self.player.current_room.get_exits()
            if next_room_id not in self.maze_graph.verticies:
                self.create_room_in_graph(next_room_id, next_room_exits)
            self.maze_graph.add_edge(room_id, next_room_id, next_dir)
            self.check_exits(room_id)

    def build_graph(self, r=None, g=None, p=None, q=None):
        if g is None:
            g = Graph()
        if p is None:
            p = Player(world.starting_room)
        if q is None:
            q = Queue()
        if r is None:
            r = p.current_room
        r_exits = p.current_room.get_exits()
        if r.id not in g.verticies:
            for r_exit in r_exits:
                g.add(r.id, r_exit)
        for direction in g.verticies[r.id]:
            q.enqueue((direction, r))

        while len(q) > 0:
            next_move = q.dequeue();
            direction = next_move[0]
            room = next_move[1]

            next_room = room.get_room_in_direction(direction)
            next_room_exits = room.get_room_in_direction(direction).get_exits()
            if next_room.id not in g.verticies:
                for r_exit in next_room_exits:
                    g.add(next_room.id, r_exit)
            g.add_edge(room.id, next_room.id, direction)
            for r_exit in g.verticies[next_room.id]:
                if g.verticies[next_room.id][r_exit] == '?':
                    q.enqueue((r_exit, next_room))

            print(f'Current Graph: {len(g.verticies)}')

    def walk_maze_for_exercise(self):
        dir_list = ['n', 'w', 'e', 's']
        for direction in dir_list:
            self.directions[direction] = direction
        room_id = self.player.current_room.id
        room_exits = self.player.current_room.get_exits()

        if room_id not in self.maze_graph.verticies:
            for an_exit in room_exits:
                self.maze_graph.add(room_id, an_exit)

        # Loop through till we have all paths explored
        while len(self.finished) != len(room_graph):
            # Move Forward to Dead End
            check = self.check_exits(room_id)
            if not check and room_id not in self.available_rooms:
                self.available_rooms.append(room_id)

            while not check:
                self.advance()
                room_id = self.player.current_room.id
                check = self.check_exits(room_id)

            while check:
                get_path_to_next_advance = self.retreat(room_id)
                # [4, 0]
                # If None
                print(get_path_to_next_advance)
                if get_path_to_next_advance is not None:
                    current_room_ids = get_path_to_next_advance[:-1]
                    next_room_ids = get_path_to_next_advance[1:]
                    # Get the Directions to Travel Back
                    next_dirs = []
                    for i in range(len(get_path_to_next_advance) - 1):
                        cur_room_id = current_room_ids[i]
                        nex_room_id = next_room_ids[i]
                        for direction in self.maze_graph.verticies[cur_room_id]:
                            if self.maze_graph.verticies[cur_room_id][direction] == nex_room_id:
                                next_dirs.append(direction)
                    for backtrack_direction in next_dirs:
                        self.player.travel(backtrack_direction)
                        print(f'Retreating to room {self.player.current_room.id}')
                        traversal_path.append(backtrack_direction)
                    room_id = self.player.current_room.id
                    check = self.check_exits(room_id)
                else:
                    break


traverse_me = Traversal(player)
traverse_me.walk_maze_for_exercise()
# traverse_me.build_graph()

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
