# Submission checklist

## Complete and verified

- [x] Separate `airlinesense-mlops` Git repository
- [x] Seven meaningful local commits
- [x] Public airline satisfaction dataset validated
- [x] Raw CSV tracked by DVC
- [x] DVC prepare, features, train, and evaluate pipeline
- [x] Three genuine MLflow model experiments
- [x] Production candidate registered in local MLflow registry
- [x] One training/inference sklearn pipeline
- [x] FastAPI `/health`, `/model-info`, and `/predict`
- [x] Streamlit calls FastAPI over HTTP
- [x] Nine automated tests pass
- [x] Docker image builds
- [x] Docker container is healthy
- [x] Real container prediction verified
- [x] Browser demo verified with no console errors
- [x] GitHub Actions CI workflow
- [x] GitHub Actions Docker Hub workflow
- [x] README and technical decisions
- [x] Demo script and instructor questions
- [x] Minimal eight-slide PowerPoint deck
- [x] Backup UI screenshot

## Account-dependent steps before submission

- [ ] Re-authenticate GitHub CLI: `gh auth login -h github.com`
- [ ] Create the personal GitHub repository `airlinesense-mlops`
- [ ] Add it as the new repository remote and push `main`
- [ ] Create Docker Hub repository `airlinesense-mlops`
- [ ] Add GitHub secrets `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`
- [ ] Run and verify both GitHub Actions workflows
- [ ] Confirm the Docker Hub `latest` and `sha-*` tags exist
- [ ] Submit the GitHub URL and Docker Hub URL

Do not claim GitHub Actions or Docker Hub success until these account steps are completed and their pages show a green result.

