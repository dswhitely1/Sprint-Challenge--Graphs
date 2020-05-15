from ast import literal_eval

from player import Player
from util import Stack, Queue
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


class Traversal:
    def __init__(self, robot):
        self.player = robot
        self.maze_graph = {}
        self.queue = Queue()
        self.stack = Stack()
        self.finished = set()
        self.reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}

    def check_exits(self, room_id):
        for exits in self.maze_graph[room_id]:
            if self.maze_graph[room_id][exits] == '?':
                return False
        self.finished.add(room_id)
        return True

    def is_transversed(self):
        for rooms in self.maze_graph:
            for directions in self.maze_graph[rooms]:
                if self.maze_graph[rooms][directions] == '?':
                    return False
        return True

    def check_maze(self, room_id, room_exits):
        if room_id not in self.maze_graph:
            self.maze_graph[room_id] = {}
            for directions in room_exits:
                self.maze_graph[room_id][directions] = '?'

    def get_next_direction(self, room_id):
        for direction in self.maze_graph[room_id]:
            if self.maze_graph[room_id][direction] == '?':
                return direction
        return None

    def retreat(self, room_id, prev_room_id=None, back_path=None, visited=None):
        if back_path is None:
            back_path = []
        if visited is None:
            visited = set()
        if room_id == 335:
            # Stop Debugger here
            print(room_id)
        check = self.check_exits(room_id)
        back_path.append(room_id)
        if len(self.finished) == len(room_graph):
            return None
        if not check:
            return back_path
        for key, value in self.maze_graph[room_id].items():
            if prev_room_id != value:
                new_path = self.retreat(value, room_id, back_path, visited)
                if new_path:
                    return new_path

    def advance(self):
        room_id = self.player.current_room.id
        room_exits = self.player.current_room.get_exits()
        if room_id not in self.maze_graph:
            self.check_maze(room_id, room_exits)

        if room_id not in self.finished and self.check_exits(room_id):
            self.finished.add(room_id)

        # Push Available Directions into The Stack

        next_dir = self.get_next_direction(room_id)
        if next_dir is not None:
            self.player.travel(next_dir)
            traversal_path.append(next_dir)
            next_room_id = self.player.current_room.id
            next_room_exits = self.player.current_room.get_exits()
            print(f'Moving Player from Room {room_id} to Room {next_room_id} in the direction of {next_dir}')
            self.check_maze(next_room_id, next_room_exits)
            self.maze_graph[room_id][next_dir] = next_room_id
            self.maze_graph[next_room_id][self.reverse_dirs[next_dir]] = room_id


    def walk_maze_for_exercise(self, room_finished=None, prev=None, path=None):
        if room_finished is None:
            room_finished = set()

        if path is None:
            path = []

        room_id = self.player.current_room.id
        room_exits = self.player.current_room.get_exits()

        if room_id not in self.maze_graph:
            self.check_maze(room_id, room_exits)

        if self.check_exits(room_id):
            room_finished.add(room_id)

        # Loop through till we have all paths explored
        while len(self.finished) != len(room_graph):
            # Move Forward to Dead End
            check = self.check_exits(room_id)
            print(self.finished)
            while not check:
                self.advance()
                room_id = self.player.current_room.id
                check = self.check_exits(room_id)

            while check:
                get_path_to_next_advance = self.retreat(room_id)
                # [4, 0]
                # If None
                if get_path_to_next_advance is not None:
                    current_room_ids = get_path_to_next_advance[:-1]
                    next_room_ids = get_path_to_next_advance[1:]
                    # Get the Directions to Travel Back
                    next_dirs = []
                    for i in range(len(get_path_to_next_advance) - 1):
                        cur_room_id = current_room_ids[i]
                        nex_room_id = next_room_ids[i]
                        for direction in self.maze_graph[cur_room_id]:
                            if self.maze_graph[cur_room_id][direction] == nex_room_id:
                                next_dirs.append(direction)
                    for backtrack_direction in next_dirs:
                        self.player.travel(backtrack_direction)
                        print(
                            f'Player Backtracking to Room {player.current_room.id} in the direction of {backtrack_direction}  Current visited room count: {len(self.finished)}')
                        print(f'Current Graph: {self.maze_graph[self.player.current_room.id]}')
                        print(f'Current Overall Graph: {self.maze_graph}')
                        traversal_path.append(backtrack_direction)
                        print(f'Number of steps: {len(traversal_path)}')
                    room_id = self.player.current_room.id
                    check = self.check_exits(room_id)
                else:
                    break


            # if room_id not in room_finished:
            #     for direction in self.maze_graph[room_id]:
            #         if direction in self.maze_graph[room_id]:
            #             if self.maze_graph[room_id][direction] == '?':
            #                 s.push(direction)
            #         else:
            #             s.push(direction)
            # else:
            #     # We're in a deadend, check maze graph for possible exits
            #     # Clear the Stack
            #     s = Stack()
            #     reverse_path = self.retreat(room_id)
            #     cur_room_path = reverse_path[:-1]
            #     next_room_path = reverse_path[1:]
            #     new_dirs = []
            #     for i in range(len(reverse_path) -1):
            #         for key, value in self.maze_graph[cur_room_path[i]]:
            #             if value == next_room_path[i]:
            #                 new_dirs.append(key)
            #     print(new_dirs)
            #     print(f'reverse_path: {reverse_path[1:]}')




        # next_dir = s.pop()
        # if next_dir is not None:
        #     self.player.travel(next_dir)
        #     traversal_path.append(next_dir)
        #     path = path + [next_dir]
        #     next_room_id = self.player.current_room.id
        #     next_room_exits = self.player.current_room.get_exits()
        #     self.check_maze(next_room_id, next_room_exits)
        #     self.maze_graph[room_id][next_dir] = next_room_id
        #     self.maze_graph[next_room_id][self.reverse_dirs[next_dir]] = room_id
        #     new_path = self.walk_maze_for_exercise(room_finished, next_dir, path, s)
        #     if new_path:
        #         return new_path


traverse_me = Traversal(player)
traverse_me.walk_maze_for_exercise()

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
