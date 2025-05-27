import React, { useEffect } from "react";
import { useState } from "react";
import { TextField } from "@mui/material"
import { Stack } from "@mui/material";
import { Autocomplete } from "@mui/material";
import { Box } from "@material-ui/core";
import axiosInstance from "../axios";

const SearchBooks = () => {
    const [books, setJsonResults] = useState([]);
    const [selected, setSelected] = useState([]);
    const handleChange = (e, newValue) => setSelected(newValue)

    useEffect(() => {
        axiosInstance.get('book-list/')
        .then((books) => setJsonResults(books.data));
        },[]);
    return (
        <Stack>
            <Autocomplete
  id="book-list"
  options={books}
  getOptionLabel={(book) => book.title || ""}
  onChange = {handleChange}
  style={{ width: 300 }}
  isOptionEqualToValue={(option, value) => 
    option.title === value.title
}
noOptionsText = {"No available book with this name"}
renderOption = {(props, books) => (
    <Box component="li" {...props} key={books.isbn}>
        {books.title}
    </Box>
)}
  renderInput={(params) => <TextField {...params} label="Select a book" variant="outlined" />}
/>
        </Stack>
    )
}
        
export default SearchBooks;
