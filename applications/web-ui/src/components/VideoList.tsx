'use client';

import * as React from 'react';
import he from 'he';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Pagination from '@mui/material/Pagination';


interface Genre {
    id: number;
    genre: string;
}

interface Video {
    id: number;
    youtube_video_id: string;
    youtube_channel_id: string;
    title: string;
    description: string;
    publish_date: Date;
    thumbnail_url: string;
    genres: Genre[];
}

interface VideoListProps {
    selectedGenre: string;
}

export default function VideoList({ selectedGenre }: VideoListProps) {
    const [data, setData] = React.useState<Video[]>([]);
    const [loading, setLoading] = React.useState(true);
    const [error, setError] = React.useState(null);
    const [page, setPage] = React.useState(1);
    const [totalItems, setTotalItems] = React.useState(0);
    const itemsPerPage = 10;

    React.useEffect(() => {
        const fetchData = async () => {
            try {
                const apiUrl = process.env.NEXT_PUBLIC_API_URL;
                console.log(`NEXT_PUBLIC_API_URL: ${apiUrl}`);

                const response = await fetch(`${apiUrl}/api/videos?genre_id=${selectedGenre}`);
                if (!response.ok) {
                    console.log(response);
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const json = await response.json();
                setData(json);
                setTotalItems(json.length);
                setPage(1);
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

    const startIndex = (page - 1) * itemsPerPage;
    const paginatedData = data.slice(startIndex, startIndex + itemsPerPage);
    const totalPages = Math.ceil(totalItems / itemsPerPage);

    return (
        <Box sx={{ pt: 4, display: 'flex', flexDirection: "column", gap: 2 }}>
            {paginatedData
            .sort((a: Video, b: Video) => new Date(b.publish_date).getTime() - new Date(a.publish_date).getTime())
            .map((video: Video) => (
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
                            .sort((a: Genre, b: Genre) => a.genre.localeCompare(b.genre))
                            .map((genre: Genre) => (
                                <Typography key={ genre.id } sx={{ px: 1.5, py: 1, borderRadius: 1, backgroundColor: '#4db6ac', color: 'white' }}>
                                    { genre.genre }
                                </Typography>
                            ))}
                        </Box>
                        <Typography variant="caption">Upload Date: { new Date(video.publish_date).toLocaleDateString() }</Typography>
                    </Box>
                </Paper>
            ))}
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
                <Pagination
                    count={totalPages}
                    page={page}
                    onChange={(event, value) => setPage(value)}
                    color="primary"
                />
            </Box>
        </Box>
    );
}
