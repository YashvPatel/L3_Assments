import random

some_animal = [
    ['Aardvark', 'cub'], ['Albatross', 'chick'], ['Alligator', 'hatchling'], ['Alpaca', 'cria'], ['Anteater', 'pup'],
    ['Antelope', 'calf'], ['Armadillo', 'pup'], ['Ass/donkey', 'foal'], ['Badger', 'cub'], ['Bat', 'pup'],
    ['Bear', 'cub'], ['Beaver', 'kit'], ['Bison', 'calf'], ['Buffalo', 'calf'], ['Camel', 'calf'], ['Caribou', 'calf'],
    ['Cat', 'kitten'], ['Cheetah', 'cub'], ['Chicken', 'chick'], ['Chimpanzee', 'infant'], ['Coyote', 'pup'],
    ['Crab', 'zoea'], ['Crocodile', 'hatchling'], ['Crow', 'chick'], ['Deer', 'fawn'], ['dog', 'puppy'],
    ['Dolphin', 'calf'], ['Dove', 'chick'], ['Dragonfly', 'nymph'], ['Duck', 'duckling'], ['Elephant', 'calf'],
    ['Elk', 'calf'], ['Ferret', 'kit'], ['Fox', 'cub'], ['Gazelle', 'calf'], ['Gerbil', 'pup'], ['Giraffe', 'calf'],
    ['Gnu', 'calf'], ['Goat', 'kid'], ['Goose', 'gosling'], ['Guinea fowl', 'keet'], ['Guinea pig', 'pup'],
    ['Gull', 'chick'], ['Hamster', 'pup'], ['Hare', 'leveret'], ['Hawk', 'eyas'], ['Hedgehog', 'hoglet'],
    ['Heron', 'chick'], ['Hippopotamus', 'calf'], ['Hornet', 'larvae']
]

current_output = random.choice(some_animal)
question = current_output[0]
right_ans = current_output[1]

all_ans = [right_ans]

print(f"Question: {question} | Right Answer: {right_ans}")

while len(all_ans) < 4:
    random_pair = random.choice(some_animal)
    random_ans = random_pair[1]

    if random_ans not in all_ans:
        all_ans.append(random_ans)

print(all_ans)