from orpheus_tts import OrpheusModel
import wave
import time

def test_basic_generation():
    try:
        print("Initializing Orpheus TTS model...")
        model = OrpheusModel(model_name="canopylabs/orpheus-tts-0.1-finetune-prod")
        
        test_text = "Hello, this is a test of the Orpheus TTS system."
        print(f"\nGenerating speech for text: {test_text}")
        
        start_time = time.monotonic()
        syn_tokens = model.generate_speech(
            prompt=test_text,
            voice="tara",
            temperature=1.0,
            top_p=0.9,
            repetition_penalty=1.1
        )
        
        print("\nSaving audio to test_output.wav...")
        with wave.open("test_output.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            
            total_frames = 0
            for audio_chunk in syn_tokens:
                frame_count = len(audio_chunk) // (wf.getsampwidth() * wf.getnchannels())
                total_frames += frame_count
                wf.writeframes(audio_chunk)
            
            duration = total_frames / wf.getframerate()
        
        end_time = time.monotonic()
        print(f"\nGeneration complete!")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print(f"Audio duration: {duration:.2f} seconds")
        print(f"Real-time factor: {(end_time - start_time) / duration:.2f}x")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")

if __name__ == "__main__":
    test_basic_generation()