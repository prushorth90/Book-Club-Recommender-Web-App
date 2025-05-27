import React, { useState } from "react";
import { makeStyles, Container} from "@material-ui/core";
import { useNavigate } from "react-router-dom";
import { FormControl } from "@mui/material";
import { InputLabel } from "@mui/material";
import { Select } from "@mui/material";
import { MenuItem } from "@mui/material";
import { Box } from "@mui/material";
import { Button } from "@mui/material";
import { useEffect } from "react";
import { Stack } from "@mui/material";
import { Autocomplete } from "@mui/material";
import { TextField } from "@mui/material";
import CssBaseline from '@material-ui/core/CssBaseline';
import RateReviewIcon from '@mui/icons-material/RateReview';
import { Grid } from "@material-ui/core";

import axiosInstance from "../axios";
import SearchBooks from "./SearchBooks";
import Template from "./Template";
import Parragraph from "./clubDisplayHelpers/Parragraph";
import Title2 from "./clubDisplayHelpers/Title2";

const useStyles = makeStyles((theme) => ({
	paper: {
		marginTop: theme.spacing(8),
		display: 'flex',
		flexDirection: 'column',
		alignItems: 'center',
	},
	avatar: {
		margin: theme.spacing(2),
	},
	form: {
		width: '100%', // Fix IE 11 issue.
		marginTop: theme.spacing(3),
	},
	submit: {
		margin: theme.spacing(3, 0, 2),
	},
}));

const RateBooks = () => {
    const navigate = useNavigate();
    
    const [formData, updateFormData] = useState([]);
    const [books, setJsonResults] = useState([]);
    const [selectedOption, SetSelectedOption] = useState([]);

    const handleChange = (e,value) => { 
        updateFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    }

    useEffect(() => {
        axiosInstance.get('book-list/')
        .then((books) => setJsonResults(books.data));
        },[]);

    const handleSubmit = (e) => {
    
        console.log(selectedOption)

        axiosInstance
        .post('book_rating/', {
            book: selectedOption.isbn,
            rating: formData.rating,

        })
        .then((res) =>{
            navigate('/rate_books')
        })

    }
    const classes=useStyles();

    return (
        <>
        
		<Template/>
		<Container component="main" maxWidth='sm' margin='100' >
			<CssBaseline />
			
			<div className={classes.paper}>
			
				<RateReviewIcon className={classes.avatar}></RateReviewIcon>
				<Title2>Rate a Book</Title2>
				<Parragraph>Get some book recommendations if you rate 3 or more! </Parragraph>
				<form className={classes.form} noValidate>
                    <Grid item xs={12} align="center">
                        <Stack>
                            <Autocomplete
                                options={books}
                                getOptionLabel={(book) => book.title || ""}
                                onChange={(_event, newBook) => {
                                    SetSelectedOption(newBook);
                                }}
                                
                                isOptionEqualToValue={(option, value) => 
                                    option.title === value.title
                                }
                                noOptionsText = {"No available book with this name"}
                                renderOption = {(props, books) => (
                                    <Box  component="li" {...props} key={books.isbn}>
                                        {books.title}
                                    </Box>
                                )}
                                renderInput={(params) => <TextField  {...params} required label="Select a book" variant="outlined"

                                />}
                                />
                        </Stack>
                    </Grid> 
                    <FormControl fullWidth>
                        <InputLabel id="demo-simple-select-label">Rating</InputLabel>
                        <Select
                            onChange={handleChange}
                            name="rating"
                            defaultValue=""
                        >
                            <MenuItem value={1}>1</MenuItem>
                            <MenuItem value={2}>2</MenuItem>
                            <MenuItem value={3}>3</MenuItem>
                            <MenuItem value={4}>4</MenuItem>
                            <MenuItem value={5}>5</MenuItem>
                            <MenuItem value={6}>6</MenuItem>
                            <MenuItem value={7}>7</MenuItem>
                            <MenuItem value={8}>8</MenuItem>
                            <MenuItem value={9}>9</MenuItem>
                            <MenuItem value={10}>10</MenuItem>

                        </Select>
                    </FormControl>
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="primary"
                        className={classes.submit}
                        onClick={handleSubmit}
                        style={{backgroundColor: '#643513',}}
                    >
                        Rate Book
					</Button>
				</form>
			</div>
		</Container>
		</>
        
    );
};

export default RateBooks;