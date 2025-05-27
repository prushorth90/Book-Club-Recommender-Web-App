import React, { useState, useEffect, useContext } from 'react';
import axiosInstance from '../axios';
import Navbar from './templateHelpers/Navbar';
import { SingleDatePicker } from 'react-dates';
import TimePicker from 'react-time-picker';
import moment from 'moment';
import { Autocomplete } from "@mui/material";

import { useNavigate, useParams, Navigate } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import { Box } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import { Check, CheckBox } from '@material-ui/icons';
import AuthContext from '../context/AuthContext';

import "react-dates/lib/css/_datepicker.css";

import 'react-dates/initialize';

import './create-meeting.css';

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function CreateMeeting() {
  let {user} = useContext(AuthContext)
  const { id } = useParams()
  const navigate = useNavigate();
  const initialFormData = Object.freeze({
    club: id,
    creator: user.username,
    date: moment(),
    time: '16:54:51',
    book: '',
    location: '',
    link_to_meeting: 'https://www.youtube.com/',
    remote: 'False',
  });

  const [isRemoteClicked, setIsRemoteClicked] = useState( false );

  const [data, setData] = useState({});
  const [bookList, setBookList] = useState([]);
  const [selectedOption, SetSelectedOption] = useState([]);
  const [userAuth, setUserAuth] = useState(null);




  useEffect(() => {
    axiosInstance.get('user-auth-detail/' + id + '/').then((res) => {
      setData(res.data);
      console.log(res.data);
    });
  }, [setData]);

  useEffect(() => {
    axiosInstance.get('book-list/')
    .then((books) => {
      console.log('books api call', books);
      setBookList(books.data)
    });
  },[]);

  useEffect(() => {
		axiosInstance.get('user-auth-detail/' + id + '/')
		.then((response) => {
		  setUserAuth(response.data.rank);
		  })
		.catch((e) => {
		  setUserAuth(e.response.data.detail);
		});
  
	  }, [setUserAuth]);



  const [formData, updateFormData] = useState(initialFormData);

  const handleRemoteClick = () => {
    setIsRemoteClicked( !isRemoteClicked );
  }

  const isFormValid = () => {
    console.log(formData);
    const required = ['date', 'books', 'time'];
    let isValid = required.reduce((valid, key) => {
      return valid && formData[key] != null && typeof formData[key] == "string" ? formData[key].length > 0 : true
    }, true)
    if(!isRemoteClicked) {
      isValid = isValid && formData.location != null && formData.location.length > 0;
    } else {
      isValid = isValid && formData.link_to_meeting != null && formData.link_to_meeting.length > 0;
    }
    console.log(isValid);
    return isValid;
  }

  const handleChange = (e) => {
    updateFormData({
      ...formData,
      // Trimming any whitespace
      [e.target.name]: e.target.value.trim(),
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('formData', formData);
    console.log('data', data);
    console.log(selectedOption)

    const postData = {
      club: id, 
      creator: user.username,
      date: formData?.date.format("YYYY-MM-DD"),
      time: formData?.time,
      book: selectedOption.isbn,
      location: formData?.location,
      link_to_meeting: formData?.link_to_meeting,
      remote: isRemoteClicked
    };

    console.log('postData', postData);

    axiosInstance
      .post('create-meeting/' + id + '/', postData)
      .then((res) => {
        console.log('navigate to dash');
        navigate(`/club/${id}`);
      }).catch((error) => {
        console.log('error', error);
        navigate(`/club/${id}`);
      })
  };

  const classes = useStyles();

  console.log('formEData', formData);

  return (
    <>
      <Navbar />
    {userAuth == 'Not found.' &&
          <Navigate to={"/club/"+id}/>
        }
         {userAuth == 'applicant' &&
          <Navigate to={"/club/"+id}/>
        }
        {userAuth != null &&
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <div className={classes.paper}>
          <Typography component="h1" variant="h5">
            Create a Meeting for your club
          </Typography>
          <form className={classes.form} noValidate>
            <Grid container spacing={2}>
              <Grid item xs={12}>
              <SingleDatePicker
                onDateChange={(date) => {
                  updateFormData({
                    ...formData,
                    date,
                  });
                }}
                numberOfMonths={1}
                horizontalMargin={0}
                date={formData.date}
                focused={true}
                hideKeyboardShortcutsPanel
                onFocusChange={(focused) => true}
                disabled={false}
                noBorder
            />
              </Grid>
              <Grid item xs={12}>
                <TimePicker disableClock onChange={time => console.log('time', time)} value={formData.time} />
              </Grid>
              <Grid item xs={12}>
              <Autocomplete
                  options={bookList}
                  getOptionLabel={(book) => book.title || ""}
                  onChange={(_event, newBook) => {
                      SetSelectedOption(newBook);
                  }}
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
                  renderInput={(params) => <TextField  {...params} required label="Book" variant="outlined" />}
                />
              </Grid>
              {!isRemoteClicked && (
                <Grid item xs={12}>
                  <TextField
                    variant="outlined"
                    required
                    fullWidth
                    id="location"
                    label="Location"
                    name="location"
                    autoComplete="location"
                    onChange={handleChange}
                    value={formData.location}
                  />
                </Grid>
              )}
              {isRemoteClicked && (
                <Grid item xs={12}>
                  <TextField
                    variant="outlined"
                    fullWidth
                    multiline
                    rows={4}
                    id="link_to_meeting"
                    label="Link To Meeting"
                    name="link_to_meeting"
                    autoComplete="link_to_meeting"
                    onChange={handleChange}
                  />
                </Grid>
              )}
             {formData.location !== '' ? null : (
                <Grid item xs={12}>
                  <p>Remote</p>
                  <input value={isRemoteClicked} type="CheckBox" onClick={handleRemoteClick} />
                </Grid>
             )}
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              disabled={!isFormValid()}
              className={classes.submit}
              onClick={handleSubmit}
            >
              Create Meeting
            </Button>
          </form>
        </div>
      </Container>
      		}
    </>
  );
}
