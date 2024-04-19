import React, { useState, useEffect } from 'react';
import Gallery from '../components/Gallery';
import SearchBar from '../components/SearchBar';
import { Container, Box, Typography } from '@mui/material';

const mockImages = [
  { id: 1, filename: 'image1.jpg', title: 'Image 1' },
  { id: 2, filename: 'image2.jpg', title: 'Image 2' }
];

const useMockData = true;

const fetchImages = () => {
  return fetch('http://localhost:5000/api/images')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .catch(error => {
      console.error('Failed to fetch images:', error);
      return mockImages;
    });
};

function Home() {
  const [images, setImages] = useState(mockImages);

  useEffect(() => {
    if (!useMockData) {
      fetchImages().then(data => {
        setImages(data);
      }).catch(error => {
        console.error('Error fetching images:', error);
      });
    }
  }, [useMockData]);

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Welcome to the Graduation Photo Wall
        </Typography>
        <SearchBar setSearchResults={setImages} />
        <Gallery images={images} />
      </Box>
    </Container>
  );
}

export default Home;
