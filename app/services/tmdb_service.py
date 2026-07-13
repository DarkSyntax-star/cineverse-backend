import httpx
from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from ..core.config import settings

class TmdbService:
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL
        self.image_base_url = settings.TMDB_IMAGE_BASE_URL

        if not self.api_key:
            raise ValueError("TMDB_API_KEY is not set in environment variables")

    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a request to the TMDB API"""
        url = f"{self.base_url}/{endpoint}"
        params = params or {}
        params["api_key"] = self.api_key
        params["language"] = "en-US"

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"TMDB API error: {e.response.text}"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"TMDB service error: {str(e)}"
                )

    def _transform_movie(self, tmdb_movie: Dict[str, Any]) -> Dict[str, Any]:
        """Transform TMDB movie data to our schema"""
        return {
            "id": tmdb_movie.get("id"),
            "title": tmdb_movie.get("title", "Unknown"),
            "description": tmdb_movie.get("overview", ""),
            "poster_url": f"{self.image_base_url}/w500{tmdb_movie.get('poster_path', '')}" if tmdb_movie.get('poster_path') else None,
            "backdrop_url": f"{self.image_base_url}/original{tmdb_movie.get('backdrop_path', '')}" if tmdb_movie.get('backdrop_path') else None,
            "trailer_url": None,
            "release_date": tmdb_movie.get("release_date"),
            "runtime": tmdb_movie.get("runtime", 0),
            "rating": tmdb_movie.get("vote_average", 0.0),
            "vote_count": tmdb_movie.get("vote_count", 0),
            "is_featured": False,
            "is_trending": False,
            "is_top_rated": False,
            "is_upcoming": False,
            "language": tmdb_movie.get("original_language", "en"),
            "country": tmdb_movie.get("origin_country", ["USA"])[0] if tmdb_movie.get("origin_country") else "USA",
        }

    async def get_popular_movies(self, page: int = 1) -> List[Dict[str, Any]]:
        """Get popular movies from TMDB"""
        data = await self._make_request("movie/popular", {"page": page})
        return [self._transform_movie(movie) for movie in data.get("results", [])]

    async def get_trending_movies(self, time_window: str = "week") -> List[Dict[str, Any]]:
        """Get trending movies from TMDB"""
        data = await self._make_request(f"trending/movie/{time_window}")
        return [self._transform_movie(movie) for movie in data.get("results", [])]

    async def get_top_rated_movies(self, page: int = 1) -> List[Dict[str, Any]]:
        """Get top rated movies from TMDB"""
        data = await self._make_request("movie/top_rated", {"page": page})
        return [self._transform_movie(movie) for movie in data.get("results", [])]

    async def get_upcoming_movies(self, page: int = 1) -> List[Dict[str, Any]]:
        """Get upcoming movies from TMDB"""
        data = await self._make_request("movie/upcoming", {"page": page})
        return [self._transform_movie(movie) for movie in data.get("results", [])]

    async def get_movie_details(self, movie_id: int) -> Dict[str, Any]:
        """Get detailed movie information from TMDB"""
        data = await self._make_request(f"movie/{movie_id}", {"append_to_response": "videos,credits"})
        movie = self._transform_movie(data)

        # Add trailer
        videos = data.get("videos", {}).get("results", [])
        trailer = next((v for v in videos if v.get("type") == "Trailer"), None)
        if trailer:
            movie["trailer_url"] = f"https://www.youtube.com/watch?v={trailer.get('key')}"

        # Add cast
        cast = data.get("credits", {}).get("cast", [])[:10]
        movie["cast"] = [
            {
                "name": actor.get("name"),
                "character": actor.get("character"),
                "profile_url": f"{self.image_base_url}/w185{actor.get('profile_path')}" if actor.get('profile_path') else None
            }
            for actor in cast
        ]

        return movie

    async def search_movies(self, query: str, page: int = 1) -> List[Dict[str, Any]]:
        """Search movies on TMDB"""
        data = await self._make_request("search/movie", {"query": query, "page": page})
        return [self._transform_movie(movie) for movie in data.get("results", [])]