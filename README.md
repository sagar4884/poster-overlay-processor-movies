Poster Overlay Processor

A Python application containerized with Docker to apply a user-provided PNG overlay (e.g., a logo, watermark, or border) to existing movie posters.

It expects the movie posters to be located in the original/ subfolder (created by the tmdb-poster-fetcher utility) and saves the result as poster.jpg in the main movie directory for local asset consumption by media servers like Plex.

Usage

This container requires two critical mappings:

Media Volume: The movie library itself (/app/data).

Overlay Volume: The PNG overlay image (/app/overlay/overlay.png).

Unraid Deployment (Example)

Repository: ghcr.io/your-username/poster-overlay-processor (after you build and push it)

Media Volume:

Host Path: /mnt/user/Media/movies

Container Path: /app/data

Overlay Volume (where your PNG is):

Host Path: /mnt/user/appdata/overlays/overlay.png

Container Path: /app/overlay/overlay.png

Environment Variable:

Key: OVERLAY_IMAGE_PATH

Value: /app/overlay/overlay.png (This is the container path to the overlay file)

This container is designed to run once and exit after processing all movies.