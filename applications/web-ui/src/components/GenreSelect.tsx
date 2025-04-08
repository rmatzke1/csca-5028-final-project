'use client';

import * as React from 'react';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import Typography from '@mui/material/Typography';


interface Genre {
    id: number;
    genre: string;
}

interface GenreSelectProps {
    selectedGenre: string;
    onGenreChange: (genre: string) => void;
}

export default function GenreSelect({ selectedGenre, onGenreChange }: GenreSelectProps) {
    const [data, setData] = React.useState<Genre[]>([]);
    const [loading, setLoading] = React.useState(true);
    const [error, setError] = React.useState(null);

    React.useEffect(() => {
        const fetchData = async () => {
            try {
                const apiUrl = process.env.NEXT_PUBLIC_API_URL;
                console.log(`NEXT_PUBLIC_API_URL: ${apiUrl}`);

                const response = await fetch(`${apiUrl}/api/genres`);
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
    }, []);

    if (loading) {
        return <Typography sx={{ mt: 3 }}>Loading genres...</Typography>;
    }

    if (error) {
        return <Typography sx={{ mt: 3, color: 'red' }}>Error loading genres: {error.message}</Typography>;
    }

    const handleChange = (event: SelectChangeEvent) => {
        onGenreChange(event.target.value);
    };

    return (
        <Select value={ selectedGenre } onChange={ handleChange } sx={{ mt: 3, minWidth: 250 }} >
            <MenuItem value="0">All genres</MenuItem>
            {data.map((genre: Genre) => (
                <MenuItem key={ genre.id } value={ genre.id }>{ genre.genre }</MenuItem>
            ))}
        </Select>
    );
}
