@echo off
echo ==================================================
echo 🚀 STARTING VIBESTREAM CD AGENT (SIMULATION)
echo ==================================================
echo.
echo [1/3] Applying Kubernetes Configurations...
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

echo.
echo [2/3] Force-Update to Latest Version...
kubectl rollout restart deployment vibestream-app

echo.
echo [3/3] Waiting for Pods to be Ready...
kubectl rollout status deployment/vibestream-app

echo.
echo ==================================================
echo ✅ APP IS LIVE!
echo 🔗 URL: http://localhost:30007
echo ==================================================
echo.
echo 💡 REAL WORLD NOTE:
echo In a real cloud setup (AWS/Azure), the cluster automatically
echo sees the new Docker image and updates itself (GitOps).
echo On your laptop, just run this script whenever you want 
echo to pull the latest updates from GitHub!
echo.
pause
