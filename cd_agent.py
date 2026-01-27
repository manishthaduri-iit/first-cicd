import time
import requests
import subprocess
import datetime

# CONFIGURATION
IMAGE_NAME = "manishthaduri26/devops-demo"
DEPLOYMENT_NAME = "vibestream-app"
CHECK_INTERVAL = 15 # Seconds

# Docker Hub API to check for image updates
API_URL = f"https://hub.docker.com/v2/repositories/{IMAGE_NAME}/tags/latest"

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}")

def get_image_digest():
    try:
        r = requests.get(API_URL)
        if r.status_code == 200:
            return r.json().get('digest')
    except Exception as e:
        log(f"Error checking Docker Hub: {e}")
    return None

def trigger_deployment():
    log("🚀 New update detected on Docker Hub!")
    log("🔄 Triggering Kubernetes Rollout...")
    
    # Force K8s to pull the new image (since tag 'latest' hasn't changed name)
    subprocess.run(f"kubectl rollout restart deployment {DEPLOYMENT_NAME}", shell=True)
    
    log("✅ Rollout triggered. App is updating...")

def main():
    print("==========================================")
    print(f"🤖 VibeStream CD Agent (GitOps)")
    print(f"👀 Watching: {IMAGE_NAME}")
    print("==========================================")
    
    current_digest = get_image_digest()
    log(f"Initial Digest: {current_digest}")

    while True:
        try:
            time.sleep(CHECK_INTERVAL)
            new_digest = get_image_digest()

            if new_digest and new_digest != current_digest:
                log(f"Hash Change Detected: {current_digest} -> {new_digest}")
                current_digest = new_digest
                trigger_deployment()
            else:
                # print(".", end="", flush=True) # Heartbeat
                pass

        except KeyboardInterrupt:
            print("\nStopping Agent.")
            break
        except Exception as e:
            log(f"Error: {e}")

if __name__ == "__main__":
    main()
