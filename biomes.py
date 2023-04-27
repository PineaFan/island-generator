class Biome:
    def __init__(self, name, temperature, humidity, precipitation, colour):
        self.name = name
        self.temperature = temperature
        self.humidity = humidity
        self.precipitation = precipitation
        self.colour = colour


class Grassland(Biome):
    def __init__(self):
        super().__init__('grassland', 20, 50, 30, "#A1CC65")


class Desert(Biome):
    def __init__(self):
        super().__init__('desert', 40, 10, 5, "#E6DC71")


class Forest(Biome):
    def __init__(self):
        super().__init__('forest', 20, 80, 60, "#60B358")


class Cliff(Biome):
    def __init__(self):
        super().__init__('swamp', 20, 90, 40, "#545454")


class Ocean(Biome):
    def __init__(self):
        super().__init__('ocean', 10, 100, 100, "#71AFE5")


class Lake(Biome):
    def __init__(self):
        super().__init__('lake', 10, 100, 100, "#78ECF2")


biomeWeights = {
    Grassland: 0.2,
    Desert: 0.3,
    Forest: 0.5,
    Cliff: 0.1,
    Lake: 0.1
}

# Create a list of all biomes, with each biome appearing in the list as many times as its weight
allBiomes = []
for biome in biomeWeights:
    for _ in range(int(biomeWeights[biome] * 100)):
        allBiomes.append(biome())

