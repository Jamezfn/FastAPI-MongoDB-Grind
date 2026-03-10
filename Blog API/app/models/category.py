from enum import Enum

class Category(str, Enum):
    TECHNOLOGY = "technology"
    SCIENCE = "science"
    HEALTH = "health"
    POLITICS = "politics"
    SPORTS = "sports"
    ENTERTAINMENT = "entertainment"