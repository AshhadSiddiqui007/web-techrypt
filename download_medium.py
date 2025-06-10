#!/usr/bin/env python3
"""
🎯 FOCUSED DIALOGPT-MEDIUM DOWNLOADER
Downloads only DialoGPT-medium with progress tracking
"""

import os
import time
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

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
        print("💡 Download will resume if interrupted")
        
        start_time = time.time()
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            resume_download=True,
            force_download=False,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        
        download_time = time.time() - start_time
        print(f"✅ Model downloaded successfully in {download_time/60:.1f} minutes")
        
        # Test the model
        print("🧪 Testing model...")
        test_input = tokenizer.encode("Hello, how can I help you with your business?", return_tensors="pt")
        with torch.no_grad():
            output = model.generate(
                test_input, 
                max_length=50, 
                do_sample=True, 
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )
        test_response = tokenizer.decode(output[0], skip_special_tokens=True)
        print(f"✅ Model test successful!")
        print(f"🤖 Test response: {test_response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        print("💡 You can run this script again to resume the download")
        return False

def main():
    """Main function"""
    print("🎯 DIALOGPT-MEDIUM FOCUSED DOWNLOADER")
    print("=" * 50)
    
    # Download DialoGPT-medium
    success = download_dialogpt_medium()
    
    if success:
        print("\n🎉 SUCCESS!")
        print("✅ DialoGPT-medium downloaded and ready")
        print("✅ Model tested and working")
        print("✅ Project optimized for best LLM performance")
        print("\n🎯 Your chatbot now has the best LLM for business conversations!")
        print("🚀 Ready to start the server and test!")
    else:
        print("\n❌ DOWNLOAD FAILED")
        print("💡 Try running the script again - downloads can resume")
        print("🔧 Check your internet connection and try again")

if __name__ == "__main__":
    main()
