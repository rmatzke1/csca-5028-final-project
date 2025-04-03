'use client';

import * as React from 'react';
import he from 'he';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';


interface VideoListProps {
    selectedGenre: number | string;
}

export default function VideoList({ selectedGenre }: VideoListProps) {
    const [data, setData] = React.useState(null);
    const [loading, setLoading] = React.useState(true);
    const [error, setError] = React.useState(null);

    React.useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`http://localhost:8000/api/videos?genre_id=${selectedGenre}`);
                if (!response.ok) {
                    console.log(response);
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const json = await response.json();
                setData(json);
            } catch (e) {
                setError(e);
                setData(null);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [selectedGenre]);

    if (loading) {
        return <Typography sx={{ mt: 3 }}>Loading videos...</Typography>;
    }

    if (error) {
        return <Typography sx={{ mt: 3, color: 'red' }}>Error loading videos: {error.message}</Typography>;
    }

    const sortedVideos = data
        ? data.sort((a: any, b: any) => new Date(b.publish_date).getTime() - new Date(a.publish_date).getTime())
        : [];

    return (
        <Box sx={{ pt: 4, display: 'flex', flexDirection: "column", gap: 2 }}>
            {sortedVideos.map((video: any) => (
                <Paper key={ video.id } elevation={4} sx={{ width: 1 }}>
                    <Box sx={{ m: 3 }}>
                        <Typography variant="h6">{ he.decode(video.title) }</Typography>
                        <Typography>{ he.decode(video.description) }</Typography>
                        <Box sx={{ my: 2 }}>
                            <Link target="_blank" href={`https://www.youtube.com/watch?v=${ video.youtube_video_id }`}>
                                <img src={ video.thumbnail_url } alt={ video.title } />
                            </Link>
                        </Box>
                        <Box sx={{ display: 'flex', flexDirection: 'row', gap: 1, marginBottom: 1 }}>
                            {video.genres
                            .sort((a, b) => a.genre.localeCompare(b.genre))
                            .map((genre: { id: number, genre: string }) => (
                                <Typography key={ genre.id } sx={{ px: 1.5, py: 1, borderRadius: 1, backgroundColor: '#4db6ac', color: 'white' }}>
                                    { genre.genre }
                                </Typography>
                            ))}
                        </Box>
                        <Typography variant="caption">Upload Date: { new Date(video.publish_date).toLocaleDateString() }</Typography>
                    </Box>
                </Paper>
            ))}
        </Box>
    );
}
