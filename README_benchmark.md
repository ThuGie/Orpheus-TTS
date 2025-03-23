# Orpheus TTS Benchmarking Suite

This benchmarking suite allows you to test and compare different configurations of the Orpheus TTS system.

## Setup

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the benchmark:
   - Edit `benchmark_config.yaml` to modify test scenarios, voices, and model configurations
   - Add or modify test scenarios with different text inputs and generation parameters
   - Adjust the list of voices to test

## Running the Benchmark

```bash
python benchmark.py
```

The benchmark will:
1. Run all configured test scenarios for each voice and model combination
2. Generate audio files in the `benchmark_results` directory
3. Create performance reports including:
   - CSV file with detailed results
   - JSON file with raw data
   - Visualizations of Real-Time Factor (RTF) and generation times
   - Summary statistics

## Understanding the Results

- **Real-Time Factor (RTF)**: The ratio of generation time to audio duration. Lower is better.
- **Generation Time**: Total time taken to generate the audio.
- **Audio Duration**: Length of the generated audio.

The results are saved in the `benchmark_results` directory:
- `benchmark_results.csv`: Detailed results in CSV format
- `benchmark_results.json`: Raw results in JSON format
- `rtf_by_voice.png`: Visualization of RTF across voices
- `generation_time_by_scenario.png`: Visualization of generation times
- `summary_statistics.csv`: Statistical summary of the results

## Customizing Tests

Modify `benchmark_config.yaml` to:
- Add new test scenarios
- Adjust generation parameters (temperature, top_p, repetition_penalty)
- Add or remove voices to test
- Configure different model variants

Each test scenario can have different:
- Text content
- Emotional markers
- Generation parameters