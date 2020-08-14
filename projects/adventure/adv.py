from room import Room
from player import Player
from world import World


import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Trying to implement without Queue or BFS that I already built
# class Queue():
#     def __init__(self):
#         self.queue = []
#
#     def enqueue(self, value):
#         self.queue.append(value)
#
#     def dequeue(self):
#         if self.size() > 0:
#             return self.queue.pop(0)
#         else:
#             return None
#
#     def size(self):
#         return len(self.queue)


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# 'visited' creates dict to record visited
# 'reverse_path' helps backtrack our steps
# 'opposite_direction' add the opposite directions to help backtrack
traversal_path = []

visited = {}
reverse_path = []
opposite_direction = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}


# add first room to visited object
visited[player.current_room.id] = player.current_room.get_exits()

# loop until we run out of rooms
while len(visited) < len(room_graph):
    if player.current_room.id not in visited:
        # add to visited object and remove from unexplored
        visited[player.current_room.id] = player.current_room.get_exits()
        previous_direction = reverse_path[-1]
        visited[player.current_room.id].remove(previous_direction)

    # after all paths explored, backtrack until we can explore from room
    if len(visited[player.current_room.id]) == 0:
        previous_direction = reverse_path[-1]
        reverse_path.pop()
        traversal_path.append(previous_direction)
        # move player to newly added previous direction in traversal path
        player.travel(previous_direction)

    # if a direction isn't explored add to the direction of traversal path and explore
    else:

        direction = visited[player.current_room.id][-1]
        visited[player.current_room.id].pop()
        traversal_path.append(direction)
        # add opposite direction to the move in the reverse path
        reverse_path.append(opposite_direction[direction])
        player.travel(direction)


# I'm making it too complicated

# def bfs(starting_vertex_id):
#     q = Queue()
#     q.enqueue([starting_vertex_id])
#     visited = set()
#     while q.size() > 0:
#         path = q.dequeue()
#         x = path[-1]
#         if x not in visited:
#             for exit in graph[x]:
#                 if graph[x][exit] == '?':
#                     return path
#             visited.add(x)
#             for exit_direction in graph[x]:
#                 new_path = list(path)
#                 new_path.append(graph[x][exit_direction])
#                 q.enqueue(new_path)
#     return None
#
# def path(path):
#     current_room = path[0]
#     directions = []
#     for room in path[1:]:
#         for exit in graph[current_room]:
#             if room == graph[current_room][exit]:
#                 directions.append(exit)
#     return directions


# TRAVERSAL TEST
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
