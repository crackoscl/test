# utils
from utils import BASE_URL, get
from utils import post

# typing
from typing import List


DOGS = "/api/v1/dogs/"
BREEDS = "/api/v1/breeds/"
ANSWER = "/api/v1/answer/"

class Dog(object):
    """
    Dog object that is composed of the id, name and breed of the dog

    To initialize:
    :param id: dog id
    :param name: dog name
    :param breed: dog breed id

    USAGE:
        >>> dog = Dog(id=1, name='Bobby', breed=1)
    """

    def __init__(self, id: int, name: str, breed: int):
        self.id = id
        self.name = name
        self.breed = breed


class Breed(object):
    """
    Breed object that is composed of the id and the name of the breed.

    To initialize:
    :param id: breed id
    :param name: breed name

    Also, breed has a list of dogs for development purposes
    :field dogs: breed dog list

    USAGE:
        >>> breed = Breed(id=1, name='Kiltro')
        >>> dog = Dog(id=1, name='Cachupin', breed=breed.id)
        >>> breed.add_dog(dog)
        >>> breed.dogs_count()
        1
    """

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.dogs: List[Dog] = []

    def add_dog(self, dog: Dog):
        self.dogs.append(dog)

    def dogs_count(self) -> int:
        return len(self.dogs)


class DogHouse(object):
    """
    Doghouse object that manipulates information on breeds and dogs.
    We expect you implement all the methods that are not implemented
    so that the flow works correctly

    DogHouse has a list of breeds and a list of dogs.
    :field breeds: breed list
    :field dogs: dog list

    USAGE:
        >>> dog_house = DogHouse()
        >>> dog_house.get_data(token='some_token')
        >>> total_dogs = dog_house.get_total_dogs()
        >>> common_breed = dog_house.get_common_breed()
        >>> common_dog_name = dog_house.get_common_dog_name()
        >>> total_breeds = dog_house.get_total_breeds()
        >>> data = {  # add some data
        ...     'total_dogs': total_dogs,
        ...     'total_breeds': total_breeds,
        ...     'common_breed': common_breed.name,
        ...     'common_dog_name': common_dog_name,
        ... }
        >>> token = 'some token'
        >>> dog_house.send_data(data=data, token=token)
    """

    def __init__(self):
        self.breeds: List[Breed] = []
        self.dogs: List[Dog] = []

    def get_data(self, token: str):
        data_dog = get(BASE_URL + DOGS, token)
        page = data_dog['next']
        while "next" in (results:=get(f"{page}",token)):
            data_dog["results"].extend(results["results"])
            if results["next"]:
                page = results["next"]
            else:
                break

        data_breeds = get(BASE_URL + BREEDS + "?limit=200", token)

        breeds = {breed["id"]: Breed(breed["id"], breed["name"]) for breed in data_breeds["results"]}
        dogs = [Dog(dog["id"], dog["name"], dog["breed"]) for dog in data_dog["results"]]
        for dog in dogs:
            breeds[dog.breed].add_dog(dog)
        self.breeds = list(breeds.values())
        self.dogs = dogs

        """
        You must get breeds and dogs data from our API: http://dogs.magnet.cl

        We recommend using the Dog and Breed classes to store
        the information, also consider the dogs and breeds fields
        of the DogHouse class to perform data manipulation.
        """

    def get_total_breeds(self) -> int:
        """
        Returns the amount of different breeds in the doghouse
        """
        # api count:186
        list_breeds = []
        for breed in self.breeds:
            if breed.name not in list_breeds:
                list_breeds.append(breed.name)
        return len(list_breeds)


    def get_total_dogs(self) -> int:
        """
        Returns the amount of dogs in the doghouse
        """
        return len(self.dogs)


    def get_common_breed(self) -> Breed:
        """
        Returns the most common breed in the doghouse
        """
        list_breeds = dict()
        num = 0
        for breed in self.breeds:
            if breed.dogs_count() > num:
                num = breed.dogs_count()
                list_breeds["breed"] = breed
        common_breed = list_breeds["breed"]

        return common_breed


    def get_common_dog_name(self) -> str:
        """
        Returns the most common dog name in the doghouse
        """
        # list_dog_names = []
        # for dog in self.dogs:
        #     list_dog_names.append(dog.name)
        # common_name = max(set(list_dog_names), key=list_dog_names.count)
        # return common_name

        dog_name = {}
        for dog in self.dogs:
            if dog.name in dog_name:
                dog_name[dog.name] = dog_name[dog.name] + 1
            else:
                dog_name[dog.name] = 1

        common_dog = max(dog_name, key=dog_name.get)
        return common_dog

    def send_data(self, data: dict, token: str):
        pass

        # post_data = post(BASE_URL+ANSWER,data,token)
        # return post_data
        """
        You must send the answers obtained from the implemented
        methods, the parameters are defined in the documentation.

        Important!! We don't tell you if the answer is correct
        """
