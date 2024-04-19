import React, { useState } from 'react';
import { TextField, Button, Box } from '@mui/material';

function SearchBar({ setSearchResults }) {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = () => {
    console.log("Search term:", searchTerm); // 或调用真实的搜索函数
    // 假设这里有一个搜索函数 fetchSearchResults
    // fetchSearchResults(searchTerm).then(data => {
    //   setSearchResults(data);
    // });
  };

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', margin: '20px 0' }}>
      <TextField
        fullWidth
        variant="outlined"
        label="Search photos"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        sx={{ mr: 2, width: '75%' }} // 控制宽度和右边距
      />
      <Button variant="contained" color="primary" onClick={handleSearch}>
        Search
      </Button>
    </Box>
  );
}

export default SearchBar;
