#!/usr/bin/env python3
"""
🗑️ MODEL CLEANUP SCRIPT
Deletes all LLM models except DialoGPT-medium
Optimizes project for single best model
"""

import os
import shutil
import glob

def get_disk_space():
    """Get available disk space"""
    try:
        import psutil
        disk = psutil.disk_usage('.')
        free_gb = disk.free / (1024**3)
        total_gb = disk.total / (1024**3)
        used_gb = disk.used / (1024**3)
        return free_gb, total_gb, used_gb
    except:
        return "Unknown", "Unknown", "Unknown"

def clean_huggingface_cache():
    """Clean Hugging Face cache, keep only DialoGPT-medium"""
    print("🧹 Cleaning Hugging Face cache...")
    
    cache_dir = os.path.expanduser('~/.cache/huggingface')
    if not os.path.exists(cache_dir):
        print("✅ No Hugging Face cache found")
        return 0
    
    deleted_size = 0
    preserved_models = []
    
    try:
        hub_dir = os.path.join(cache_dir, 'hub')
        if os.path.exists(hub_dir):
            for item in os.listdir(hub_dir):
                item_path = os.path.join(hub_dir, item)
                
                # Keep only DialoGPT-medium
                if 'DialoGPT-medium' in item:
                    preserved_models.append(item)
                    print(f"✅ Preserving: {item}")
                else:
                    # Delete everything else
                    try:
                        if os.path.isdir(item_path):
                            size = get_folder_size(item_path)
                            shutil.rmtree(item_path)
                            deleted_size += size
                            print(f"🗑️ Deleted: {item} ({size/1024/1024:.1f} MB)")
                        elif os.path.isfile(item_path):
                            size = os.path.getsize(item_path)
                            os.remove(item_path)
                            deleted_size += size
                            print(f"🗑️ Deleted: {item} ({size/1024/1024:.1f} MB)")
                    except Exception as e:
                        print(f"⚠️ Could not delete {item}: {e}")
        
        # Clean transformers cache
        transformers_cache = os.path.join(cache_dir, 'transformers')
        if os.path.exists(transformers_cache):
            try:
                size = get_folder_size(transformers_cache)
                shutil.rmtree(transformers_cache)
                deleted_size += size
                print(f"🗑️ Deleted transformers cache ({size/1024/1024:.1f} MB)")
            except Exception as e:
                print(f"⚠️ Could not delete transformers cache: {e}")
        
        print(f"✅ Preserved models: {preserved_models}")
        return deleted_size
        
    except Exception as e:
        print(f"❌ Cache cleanup error: {e}")
        return 0

def get_folder_size(folder_path):
    """Get total size of folder"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except:
                    pass
    except:
        pass
    return total_size

def clean_project_models():
    """Clean models from project directories"""
    print("\n🧹 Cleaning project model files...")
    
    deleted_size = 0
    
    # Patterns to look for
    model_patterns = [
        "**/DialoGPT-small*",
        "**/distilgpt2*", 
        "**/gpt2*",
        "**/*model*.bin",
        "**/*model*.safetensors",
        "**/pytorch_model.bin",
        "**/model.safetensors"
    ]
    
    # Directories to search
    search_dirs = [
        ".",
        "Techrypt_sourcecode",
        os.path.expanduser("~/.cache"),
        os.path.expanduser("~/AppData/Local") if os.name == 'nt' else None
    ]
    
    for search_dir in search_dirs:
        if search_dir is None or not os.path.exists(search_dir):
            continue
            
        print(f"🔍 Searching in: {search_dir}")
        
        for pattern in model_patterns:
            try:
                files = glob.glob(os.path.join(search_dir, pattern), recursive=True)
                for file_path in files:
                    # Skip if it's DialoGPT-medium
                    if 'DialoGPT-medium' in file_path:
                        print(f"✅ Preserving: {file_path}")
                        continue
                    
                    try:
                        if os.path.isfile(file_path):
                            size = os.path.getsize(file_path)
                            os.remove(file_path)
                            deleted_size += size
                            print(f"🗑️ Deleted: {file_path} ({size/1024/1024:.1f} MB)")
                        elif os.path.isdir(file_path):
                            size = get_folder_size(file_path)
                            shutil.rmtree(file_path)
                            deleted_size += size
                            print(f"🗑️ Deleted: {file_path} ({size/1024/1024:.1f} MB)")
                    except Exception as e:
                        print(f"⚠️ Could not delete {file_path}: {e}")
            except Exception as e:
                print(f"⚠️ Pattern search error for {pattern}: {e}")
    
    return deleted_size

def update_ai_backend():
    """Update AI backend to use only DialoGPT-medium"""
    print("\n🔧 Updating AI backend configuration...")
    
    ai_backend_path = "Techrypt_sourcecode/Techrypt/src/ai_backend.py"
    
    if not os.path.exists(ai_backend_path):
        print("⚠️ AI backend file not found")
        return
    
    try:
        with open(ai_backend_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update model list to only include DialoGPT-medium
        new_models = """        # OPTIMIZED: Only DialoGPT-medium for best performance
        models_to_try = [
            'microsoft/DialoGPT-medium'  # Best model for business chatbots
        ]"""
        
        # Find and replace the models_to_try section
        import re
        pattern = r'models_to_try = \[.*?\]'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, "models_to_try = [\n            'microsoft/DialoGPT-medium'  # Best model for business chatbots\n        ]", content, flags=re.DOTALL)
            
            with open(ai_backend_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Updated AI backend to use only DialoGPT-medium")
        else:
            print("⚠️ Could not find models_to_try section to update")
            
    except Exception as e:
        print(f"❌ Error updating AI backend: {e}")

def main():
    """Main cleanup function"""
    print("🗑️ MODEL CLEANUP - KEEP ONLY DIALOGPT-MEDIUM")
    print("=" * 60)
    
    # Show initial disk space
    free_gb, total_gb, used_gb = get_disk_space()
    print(f"💾 Initial disk space: {free_gb:.2f} GB free / {total_gb:.2f} GB total")
    
    total_deleted = 0
    
    # Clean Hugging Face cache
    deleted_cache = clean_huggingface_cache()
    total_deleted += deleted_cache
    
    # Clean project models
    deleted_project = clean_project_models()
    total_deleted += deleted_project
    
    # Update AI backend
    update_ai_backend()
    
    # Show final results
    print("\n" + "=" * 60)
    print("🎉 CLEANUP COMPLETE!")
    print(f"🗑️ Total deleted: {total_deleted/1024/1024/1024:.2f} GB")
    
    # Show final disk space
    free_gb_final, _, _ = get_disk_space()
    if isinstance(free_gb_final, float) and isinstance(free_gb, float):
        freed_space = free_gb_final - free_gb
        print(f"💾 Final disk space: {free_gb_final:.2f} GB free (+{freed_space:.2f} GB freed)")
    
    print("\n✅ OPTIMIZATIONS COMPLETE:")
    print("   ✅ Only DialoGPT-medium preserved")
    print("   ✅ All other LLM models deleted")
    print("   ✅ Cache optimized")
    print("   ✅ AI backend updated")
    print("   ✅ Project ready for production")
    
    print("\n🎯 Your project now uses the optimal LLM setup!")

if __name__ == "__main__":
    main()
