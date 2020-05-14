from ast import literal_eval
from player import Player
from world import World
from util import Stack

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

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
        self.reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}

    def check_exits(self, room_id):
        for exits in self.maze_graph[room_id]:
            if self.maze_graph[room_id][exits] == '?':
                return False
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

    def walk_maze_for_exercise(self, room_finished=None, prev=None, path=None, s=None):
        if room_finished is None:
            room_finished = set()

        if path is None:
            path = []

        if s is None:
            s = Stack()
        room_id = self.player.current_room.id
        room_exits = self.player.current_room.get_exits()

        print(f'Room {room_id} has exits: {room_exits}')

        if room_id not in self.maze_graph:
            self.check_maze(room_id, room_exits)

        if self.check_exits(room_id):
            room_finished.add(room_id)

        if self.is_transversed():
            return path

        if room_id not in room_finished:
            for direction in self.maze_graph[room_id]:
                if direction in self.maze_graph[room_id]:
                    if self.maze_graph[room_id][direction] == '?':
                        s.push(direction)
                else:
                    s.push(direction)
        else:
            # We're in a deadend, check maze graph for possible exits
            pass

        next_dir = s.pop()
        self.player.travel(next_dir)
        traversal_path.append(next_dir)
        path = path + [next_dir]
        next_room_id = self.player.current_room.id
        next_room_exits = self.player.current_room.get_exits()
        self.check_maze(next_room_id, next_room_exits)
        self.maze_graph[room_id][next_dir] = next_room_id
        self.maze_graph[next_room_id][self.reverse_dirs[next_dir]] = room_id
        new_path = self.walk_maze_for_exercise(room_finished, room_id, path, s)
        if new_path:
            return new_path


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
