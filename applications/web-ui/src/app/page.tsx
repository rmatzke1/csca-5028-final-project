'use client';

import * as React from 'react';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import GenreSelect from '@/components/GenreSelect';
import VideoList from '@/components/VideoList';


export default function Home() {
    const [selectedGenre, setSelectedGenre] = React.useState<number | string>('0');
    const handleGenreChange = (genre: number | string) => {
        setSelectedGenre(genre);
    };

    return (
        <Container sx={{ my: 5 }}>
            <Typography variant="h3">Recap Aggregator</Typography>
            <Typography variant="h5">CSCA 5028 Final Project - Ryan Matzke</Typography>
            <GenreSelect selectedGenre={ selectedGenre } onGenreChange={ handleGenreChange } />
            <VideoList selectedGenre={ selectedGenre } />
        </Container>
    );
}
