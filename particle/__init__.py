"""Particle system module for physics-based effects."""

from dataclasses import dataclass, field
from typing import List, Tuple
from enum import Enum
import random

from config import Config
from utils import Vec2


class ParticleEffect(Enum):
    """Types of particle effects."""
    BLOOD = "blood"
    SPARKS = "sparks"
    DEBRIS = "debris"
    PULSE_BEAM = "pulse_beam"
    SHOTGUN_SPREAD = "shotgun_spread"
    PLASMA_EXPLOSION = "plasma_explosion"
    SMOKE = "smoke"


@dataclass
class Particle:
    """A single particle in the system."""
    pos: Tuple[float, float]
    velocity: Tuple[float, float]
    life: float
    max_life: float
    color: str = "green"
    size: float = 1.0
    decay: float = 0.05
    gravity: float = 0.5
    bounce: float = 0.7
    
    def update(self, dt: float) -> bool:
        """Update particle physics. Returns False when expired."""
        # Apply gravity
        vx, vy = self.velocity
        vy += self.gravity * dt
        
        # Update position
        x, y = self.pos
        x += vx * dt
        y += vy * dt
        
        # Apply decay
        self.life -= dt
        
        # Check if expired
        if self.life <= 0:
            return False
        
        # Store updated position
        self.pos = (x, y)
        self.velocity = (vx, vy)
        
        return True


class ParticleEngine:
    """Manages particle system with physics simulation."""
    
    _particles: List[Particle] = []
    _max_particles = 500
    
    @classmethod
    def spawn(cls, pos: Tuple[float, float], effect: ParticleEffect) -> None:
        """Spawn particles for the given effect."""
        # Limit total particles
        if len(cls._particles) >= cls._max_particles:
            cls._particles = cls._particles[:cls._max_particles - 100]
        
        if effect == ParticleEffect.BLOOD:
            # Blood particles
            for _ in range(random.randint(5, 15)):
                vx = random.uniform(-20, 20)
                vy = random.uniform(-30, -10)
                life = random.uniform(0.5, 1.5)
                cls._particles.append(Particle(
                    pos=pos,
                    velocity=(vx, vy),
                    life=life,
                    max_life=life,
                    color="red",
                    size=random.uniform(0.5, 1.5),
                    decay=0.1
                ))
        
        elif effect == ParticleEffect.SPARKS:
            # Sparks
            for _ in range(random.randint(3, 8)):
                vx = random.uniform(-50, 50)
                vy = random.uniform(-50, 50)
                life = random.uniform(0.2, 0.8)
                cls._particles.append(Particle(
                    pos=pos,
                    velocity=(vx, vy),
                    life=life,
                    max_life=life,
                    color="yellow",
                    size=random.uniform(0.3, 0.8),
                    decay=0.2
                ))
        
        elif effect == ParticleEffect.DEBRIS:
            # Debris
            for _ in range(random.randint(8, 20)):
                vx = random.uniform(-30, 30)
                vy = random.uniform(-40, -20)
                life = random.uniform(1.0, 2.0)
                cls._particles.append(Particle(
                    pos=pos,
                    velocity=(vx, vy),
                    life=life,
                    max_life=life,
                    color="gray",
                    size=random.uniform(0.5, 1.2),
                    decay=0.08
                ))
        
        elif effect == ParticleEffect.PULSE_BEAM:
            # Pulse beam trail
            for _ in range(random.randint(2, 5)):
                vx = random.uniform(-5, 5)
                vy = random.uniform(-5, 5)
                life = random.uniform(0.3, 0.7)
                cls._particles.append(Particle(
                    pos=pos,
                    velocity=(vx, vy),
                    life=life,
                    max_life=life,
                    color="cyan",
                    size=random.uniform(0.2, 0.6),
                    decay=0.15
                ))
        
        elif effect == ParticleEffect.SHOTGUN_SPREAD:
            # Shotgun pellets
            for _ in range(random.randint(3, 7)):
                vx = random.uniform(-10, 10)
                vy = random.uniform(-10, 10)
                life = random.uniform(0.5, 1.0)
                cls._particles.append(Particle(
                    pos=pos,
                    velocity=(vx, vy),
                    life=life,
                    max_life=life,
                    color="orange",
                    size=random.uniform(0.4, 0.9),
                    decay=0.1
                ))
        
        elif effect == ParticleEffect.PLASMA_EXPLOSION:
            # Plasma explosion
            for _ in range(random.randint(10, 25)):
                vx = random.uniform(-40, 40)
                vy = random.uniform(-40, 40)
                life = random.uniform(0.8, 1.8)
                cls._particles.append(Particle(
                    pos=pos,
                    velocity=(vx, vy),
                    life=life,
                    max_life=life,
                    color="purple",
                    size=random.uniform(0.8, 1.5),
                    decay=0.05
                ))
        
        elif effect == ParticleEffect.SMOKE:
            # Smoke
            for _ in range(random.randint(5, 15)):
                vx = random.uniform(-10, 10)
                vy = random.uniform(-5, 5)
                life = random.uniform(1.5, 3.0)
                cls._particles.append(Particle(
                    pos=pos,
                    velocity=(vx, vy),
                    life=life,
                    max_life=life,
                    color="white",
                    size=random.uniform(1.0, 2.0),
                    decay=0.03
                ))
    
    @classmethod
    def update(cls, dt: float) -> List[Particle]:
        """Update all particles and return remaining ones."""
        # Update each particle
        alive = []
        for particle in cls._particles:
            if particle.update(dt):
                alive.append(particle)
        
        cls._particles = alive
        return cls._particles
    
    @classmethod
    def clear(cls) -> None:
        """Clear all particles."""
        cls._particles = []
