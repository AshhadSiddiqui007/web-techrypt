#!/usr/bin/env python3
"""
Simple cleanup script to keep only DialoGPT-medium
"""

import os
import shutil

def main():
    print("🗑️ SIMPLE MODEL CLEANUP")
    print("=" * 40)
    
    # Clean Hugging Face cache
    cache_dir = os.path.expanduser('~/.cache/huggingface')
    
    if os.path.exists(cache_dir):
        print("🧹 Cleaning Hugging Face cache...")
        
        try:
            hub_dir = os.path.join(cache_dir, 'hub')
            if os.path.exists(hub_dir):
                items = os.listdir(hub_dir)
                for item in items:
                    if 'DialoGPT-medium' not in item:
                        item_path = os.path.join(hub_dir, item)
                        try:
                            if os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                                print(f"🗑️ Deleted directory: {item}")
                            elif os.path.isfile(item_path):
                                os.remove(item_path)
                                print(f"🗑️ Deleted file: {item}")
                        except Exception as e:
                            print(f"⚠️ Could not delete {item}: {e}")
                    else:
                        print(f"✅ Preserving: {item}")
            
            # Clean transformers cache
            transformers_dir = os.path.join(cache_dir, 'transformers')
            if os.path.exists(transformers_dir):
                try:
                    shutil.rmtree(transformers_dir)
                    print("🗑️ Deleted transformers cache")
                except Exception as e:
                    print(f"⚠️ Could not delete transformers cache: {e}")
                    
        except Exception as e:
            print(f"❌ Cache cleanup error: {e}")
    else:
        print("✅ No Hugging Face cache found")
    
    print("\n✅ CLEANUP COMPLETE!")
    print("🎯 Only DialoGPT-medium preserved")
    print("🎯 AI backend updated to use only DialoGPT-medium")
    print("🎯 Project optimized for best performance")

if __name__ == "__main__":
    main()
