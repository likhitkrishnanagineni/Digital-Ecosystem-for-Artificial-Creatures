import requests
import json
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Species:
    name: str
    energy: int = 100
    intelligence: int = 50
    cooperation: int = 50
    aggression: int = 50
    x: float = 0.0
    y: float = 0.0
    generation: int = 1
    
class EcosystemSimulation:
    def __init__(self):
        self.species = []
        self.environment = {"food": 1000, "threats": 3, "temperature": 20}
        self.history = {"populations": [], "avg_intelligence": [], "generations": []}
        
    def query_llama(self, prompt: str) -> str:
        """Query Llama 3.2 via Ollama API"""
        try:
            response = requests.post('http://localhost:11434/api/generate', 
                json={
                    'model': 'llama3.2',
                    'prompt': prompt,
                    'stream': False,
                    'options': {'temperature': 0.7, 'num_predict': 50}
                })
            return response.json()['response'].strip()
        except:
            return "survive"  # fallback
    
    def create_species(self, name: str, traits: Dict) -> Species:
        """Create a new species with AI-driven personality"""
        species = Species(
            name=name,
            intelligence=traits.get('intelligence', random.randint(30, 70)),
            cooperation=traits.get('cooperation', random.randint(20, 80)),
            aggression=traits.get('aggression', random.randint(10, 60)),
            x=random.uniform(-10, 10),
            y=random.uniform(-10, 10)
        )
        self.species.append(species)
        return species
    
    def species_decision(self, species: Species) -> str:
        """Let AI decide species behavior based on environment"""
        context = f"""
        You are {species.name}, an artificial species in a digital ecosystem.
        Your stats: Energy={species.energy}, Intelligence={species.intelligence}, 
        Cooperation={species.cooperation}, Aggression={species.aggression}
        Environment: Food={self.environment['food']}, Threats={self.environment['threats']}, 
        Temperature={self.environment['temperature']}°C
        
        Choose ONE action: hunt, gather, socialize, hide, migrate, reproduce
        
        Respond only with the option
        For example if you should hunt, just reply "hunt"
        Don't use any other word, just the action.
        """
        
        return self.query_llama(context).lower().split()[0]
    
    def execute_action(self, species: Species, action: str):
        """Execute species action and update stats"""
        if action == "hunt":
            if random.random() < 0.6:
                species.energy += 20
                species.aggression += 1
            else:
                species.energy -= 10
                
        elif action == "gather":
            if self.environment['food'] > 0:
                species.energy += 15
                self.environment['food'] -= 10
                species.cooperation += 1
                
        elif action == "socialize":
            nearby = [s for s in self.species if s != species and 
                     abs(s.x - species.x) + abs(s.y - species.y) < 5]
            if nearby:
                species.cooperation += 2
                species.intelligence += 1
                
        elif action == "hide":
            species.energy -= 5
            species.aggression -= 1
            
        elif action == "migrate":
            species.x += random.uniform(-3, 3)
            species.y += random.uniform(-3, 3)
            species.energy -= 8
            
        elif action == "reproduce":
            if species.energy > 80 and random.random() < 0.3:
                self.reproduce_species(species)
    
    def reproduce_species(self, parent: Species):
        """Create offspring with evolved traits"""
        mutation = random.uniform(0.8, 1.2)
        child = Species(
            name=f"{parent.name}_{parent.generation+1}",
            energy=60,
            intelligence=int(parent.intelligence * mutation),
            cooperation=int(parent.cooperation * mutation),
            aggression=int(parent.aggression * mutation),
            x=parent.x + random.uniform(-2, 2),
            y=parent.y + random.uniform(-2, 2),
            generation=parent.generation + 1
        )
        self.species.append(child)
        parent.energy -= 30
    
    def update_environment(self):
        """Dynamic environment changes"""
        self.environment['food'] += random.randint(50, 150)
        self.environment['threats'] = max(0, self.environment['threats'] + random.randint(-1, 2))
        self.environment['temperature'] += random.uniform(-2, 2)
        
        # Remove dead species
        self.species = [s for s in self.species if s.energy > 0]
    
    def run_simulation(self, steps: int = 20):
        """Run the ecosystem simulation"""
        print("🌍 Starting AI Species Ecosystem Simulation...")
        
        # Initialize species
        initial_species = [
            {"name": "Hunters", "intelligence": 45, "aggression": 70, "cooperation": 30},
            {"name": "Gatherers", "intelligence": 60, "cooperation": 70, "aggression": 20},
            {"name": "Nomads", "intelligence": 55, "cooperation": 40, "aggression": 40}
        ]
        
        for spec in initial_species:
            for i in range(3):  # 3 of each type
                self.create_species(f"{spec['name']}{i+1}", spec)
        
        # Simulation loop
        for step in range(steps):
            print(f"\n--- Generation {step+1} ---")
            
            # Each species makes AI-driven decisions
            for species in self.species[:]:  # Copy list to avoid modification issues
                if species.energy > 0:
                    action = self.species_decision(species)
                    self.execute_action(species, action)
                    species.energy -= 5  # Basic metabolism
                    
                    print(f"{species.name}: {action} (E:{species.energy}, I:{species.intelligence})")
            
            self.update_environment()
            
            # Record statistics
            self.history['populations'].append(len(self.species))
            avg_intel = np.mean([s.intelligence for s in self.species]) if self.species else 0
            self.history['avg_intelligence'].append(avg_intel)
            self.history['generations'].append(step+1)
            
            print(f"Population: {len(self.species)}, Avg Intelligence: {avg_intel:.1f}")
            print(f"Environment - Food: {self.environment['food']}, Temp: {self.environment['temperature']:.1f}°C")
            
            time.sleep(0.5)  # Pause for readability
        
        self.visualize_results()
    
    def visualize_results(self):
        """Create visualization of ecosystem evolution"""
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        # Population over time
        ax1.plot(self.history['generations'], self.history['populations'], 'b-o')
        ax1.set_title('Population Evolution')
        ax1.set_xlabel('Generation')
        ax1.set_ylabel('Population')
        ax1.grid(True)
        
        # Intelligence evolution
        ax2.plot(self.history['generations'], self.history['avg_intelligence'], 'r-o')
        ax2.set_title('Average Intelligence Evolution')
        ax2.set_xlabel('Generation')
        ax2.set_ylabel('Intelligence')
        ax2.grid(True)
        
        # Species distribution
        if self.species:
            x_pos = [s.x for s in self.species]
            y_pos = [s.y for s in self.species]
            colors = [s.intelligence for s in self.species]
            scatter = ax3.scatter(x_pos, y_pos, c=colors, cmap='viridis', alpha=0.6)
            ax3.set_title('Species Distribution (colored by intelligence)')
            ax3.set_xlabel('X Position')
            ax3.set_ylabel('Y Position')
            plt.colorbar(scatter, ax=ax3)
        
        plt.tight_layout()
        plt.show()
        
        # Final statistics
        print(f"\n🎯 SIMULATION COMPLETE!")
        print(f"Final population: {len(self.species)}")
        if self.species:
            print(f"Highest intelligence: {max(s.intelligence for s in self.species)}")
            print(f"Most cooperative: {max(s.cooperation for s in self.species)}")
            print(f"Latest generation: {max(s.generation for s in self.species)}")

# Run the simulation
if __name__ == "__main__":
    ecosystem = EcosystemSimulation()
    ecosystem.run_simulation(steps=50)