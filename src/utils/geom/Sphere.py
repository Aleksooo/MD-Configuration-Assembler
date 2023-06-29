from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import numpy as np
# from scipy.spatial import distance
from .Shape import Shape

@dataclass
class Sphere(Shape):
    radius: float = 0

    def get_volume(self) -> float:
        return 4/3*np.pi*self.radius**3

    def get_surface(self) -> float:
        return 4*np.pi*self.radius**2

    def check_point(self, point) -> bool:
        return np.linalg.norm(point - self.center) < self.radius
        # return distance.euclidean() < self.radius

    def generate_point(self) -> np.array:
        r = np.random.uniform(0, self.radius)
        phi = np.random.uniform(0, 2*np.pi)
        cos_theta = np.random.uniform(-1, 1)
        sin_theta = np.sqrt(1 - cos_theta**2)
        return r * np.array([
            sin_theta * np.cos(phi),
            sin_theta * np.sin(phi),
            cos_theta
            ]) + self.center
