
# 🍌 OmegaFold on Banana

This is a repo that lets you run [OmegaFold](https://github.com/HeliXonProtein/OmegaFold) on [Banana](https://banana.dev), which is a platform to run GPU accelerated code serverlessly. This essentially means you have a quick, autoscaling API to run OmegaFold.

It takes ~3 minutes to get the model loaded and ready for inference; so expect your first call after cold start to take a while. API calls right after that should be quick! You can change the `IDLE TIMEOUT` in Banana settings, which is 10s by default (i.e your instance will shut down after 10s of no activity, and will be cold booted again next time you call it.)