#!/usr/bin/env python3
"""
🎯 FOCUSED DIALOGPT-MEDIUM DOWNLOADER
Downloads only DialoGPT-medium, deletes other models
"""

import os
import shutil
import time
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def clean_cache():
    """Clean Hugging Face cache to free space"""
    print("🧹 Cleaning Hugging Face cache...")
    
    cache_dir = os.path.expanduser('~/.cache/huggingface')
    if os.path.exists(cache_dir):
        try:
            # Keep only DialoGPT-medium if it exists
            medium_path = os.path.join(cache_dir, 'hub', 'models--microsoft--DialoGPT-medium')
            medium_exists = os.path.exists(medium_path)
            
            if medium_exists:
                print(f"✅ Preserving DialoGPT-medium cache at: {medium_path}")
                # Move it to temp location
                temp_path = os.path.join(os.path.dirname(cache_dir), 'temp_medium')
                if os.path.exists(temp_path):
                    shutil.rmtree(temp_path)
                shutil.move(medium_path, temp_path)
            
            # Clean entire cache
            shutil.rmtree(cache_dir)
            print("✅ Cleaned Hugging Face cache")
            
            # Restore DialoGPT-medium if it existed
            if medium_exists:
                os.makedirs(os.path.dirname(medium_path), exist_ok=True)
                shutil.move(temp_path, medium_path)
                print("✅ Restored DialoGPT-medium cache")
                
        except Exception as e:
            print(f"⚠️ Cache cleanup warning: {e}")
    
    print("🎯 Cache optimized for DialoGPT-medium only")

def download_dialogpt_medium():
    """Download DialoGPT-medium with progress tracking"""
    print("🎯 DOWNLOADING DIALOGPT-MEDIUM")
    print("=" * 50)
    
    model_name = "microsoft/DialoGPT-medium"
    
    try:
        print(f"📥 Downloading tokenizer for {model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            resume_download=True,
            force_download=False
        )
        print("✅ Tokenizer downloaded successfully")
        
        print(f"📥 Downloading model for {model_name}...")
        print("⏳ This may take 30-60 minutes depending on connection speed...")
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            resume_download=True,
            force_download=False,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        print("✅ Model downloaded successfully")
        
        # Test the model
        print("🧪 Testing model...")
        test_input = tokenizer.encode("Hello, how can I help you?", return_tensors="pt")
        with torch.no_grad():
            output = model.generate(test_input, max_length=50, do_sample=True, temperature=0.7)
        test_response = tokenizer.decode(output[0], skip_special_tokens=True)
        print(f"✅ Model test successful: {test_response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def get_disk_space():
    """Get available disk space"""
    try:
        import psutil
        disk = psutil.disk_usage('.')
        free_gb = disk.free / (1024**3)
        return free_gb
    except:
        return "Unknown"

def main():
    """Main function"""
    print("🎯 DIALOGPT-MEDIUM FOCUSED DOWNLOADER")
    print("=" * 50)
    
    # Check disk space
    free_space = get_disk_space()
    print(f"💾 Available disk space: {free_space:.2f} GB")
    
    if isinstance(free_space, float) and free_space < 2:
        print("⚠️ WARNING: Low disk space! DialoGPT-medium needs ~1.2GB")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("❌ Download cancelled")
            return
    
    # Clean cache first
    clean_cache()
    
    # Download DialoGPT-medium
    print("\n🚀 Starting DialoGPT-medium download...")
    success = download_dialogpt_medium()
    
    if success:
        print("\n🎉 SUCCESS!")
        print("✅ DialoGPT-medium downloaded and ready")
        print("✅ Cache optimized (other models removed)")
        print("✅ Model tested and working")
        print("\n🎯 Your project now has the best LLM for business chatbots!")
    else:
        print("\n❌ DOWNLOAD FAILED")
        print("💡 Try running the script again - downloads can resume")

if __name__ == "__main__":
    main()
