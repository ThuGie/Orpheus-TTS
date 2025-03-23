import yaml
import time
import wave
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from orpheus_tts import OrpheusModel

class OrpheusBenchmark:
    def __init__(self, config_path='benchmark_config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.results = []
        self.output_dir = self.config['output_directory']
        os.makedirs(self.output_dir, exist_ok=True)
        
    def run_benchmark(self):
        for model_config in self.config['model_configs']:
            print(f"\nTesting model: {model_config['name']}")
            model = OrpheusModel(model_name=model_config['model_path'])
            
            for scenario in tqdm(self.config['test_scenarios'], desc='Scenarios'):
                for voice in self.config['voices']:
                    result = self.run_single_test(model, scenario, voice)
                    result['model'] = model_config['name']
                    self.results.append(result)
                    
        self.save_results()
        self.generate_reports()
    
    def run_single_test(self, model, scenario, voice):
        output_file = os.path.join(
            self.output_dir,
            f"{scenario['name']}_{voice}_{int(time.time())}.wav"
        )
        
        start_time = time.monotonic()
        syn_tokens = model.generate_speech(
            prompt=scenario['text'],
            voice=voice,
            temperature=scenario['temperature'],
            top_p=scenario['top_p'],
            repetition_penalty=scenario['repetition_penalty']
        )
        
        total_frames = 0
        with wave.open(output_file, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            
            for audio_chunk in syn_tokens:
                frame_count = len(audio_chunk) // (wf.getsampwidth() * wf.getnchannels())
                total_frames += frame_count
                wf.writeframes(audio_chunk)
                
        end_time = time.monotonic()
        generation_time = end_time - start_time
        audio_duration = total_frames / 24000  # 24kHz sample rate
        
        return {
            'scenario': scenario['name'],
            'voice': voice,
            'generation_time': generation_time,
            'audio_duration': audio_duration,
            'rtf': generation_time / audio_duration if audio_duration > 0 else float('inf'),
            'output_file': output_file
        }
    
    def save_results(self):
        df = pd.DataFrame(self.results)
        df.to_csv(os.path.join(self.output_dir, 'benchmark_results.csv'), index=False)
        
        with open(os.path.join(self.output_dir, 'benchmark_results.json'), 'w') as f:
            json.dump(self.results, f, indent=2)
    
    def generate_reports(self):
        df = pd.DataFrame(self.results)
        
        # RTF by voice and model
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x='voice', y='rtf', hue='model')
        plt.title('Real-Time Factor by Voice and Model')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'rtf_by_voice.png'))
        
        # Generation time by scenario
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x='scenario', y='generation_time', hue='model')
        plt.title('Generation Time by Scenario and Model')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'generation_time_by_scenario.png'))
        
        # Summary statistics
        summary = df.groupby(['model', 'scenario'])[
            ['generation_time', 'audio_duration', 'rtf']
        ].describe()
        summary.to_csv(os.path.join(self.output_dir, 'summary_statistics.csv'))

if __name__ == '__main__':
    benchmark = OrpheusBenchmark()
    benchmark.run_benchmark()