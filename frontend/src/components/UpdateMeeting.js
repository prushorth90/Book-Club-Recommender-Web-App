import React, { useState, useEffect } from 'react';
import axiosInstance from '../axios';
import { useParams } from 'react-router-dom';
//MaterialUI
import { useNavigate, Navigate } from 'react-router-dom';
import Parragraph from "./clubDisplayHelpers/Parragraph";
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import Title2 from "./clubDisplayHelpers/Title2";
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import EditIcon from '@mui/icons-material/Edit';
import Template from './Template';

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

export default function UpdateMeeting() {
  	const { id } = useParams();
	const navigate = useNavigate();

	const initialFormData = Object.freeze({
		date: '',
		time: '',
		book: '',
    location: '',
    link_to_meeting: '',



	});

	const [formData, updateFormData] = useState(initialFormData);
	const [userAuth, setUserAuth] = useState(null);


	useEffect(() => {
		axiosInstance.get('show-edit-meeting/'+ id +'/' ).then((res) => {
			console.log(res.data);
      console.log(res.data.location);
      updateFormData({
				...formData,
				['date']: res.data.date,
				['time']: res.data.time,
				['book']: res.data.book,
				['location']: res.data.location,
				['link_to_meeting']: res.data.link_to_meeting,
			});
		});
	}, [updateFormData]);

	useEffect(() => {
		axiosInstance.get('user-auth-detail/' + id + '/')
		.then((response) => {
		  setUserAuth(response.data.rank);
		  })
		.catch((e) => {
		  setUserAuth(e.response.data.detail);
		});
  
	  }, [setUserAuth]);

	const handleChange = (e) => {
		updateFormData({
			...formData,
			// Trimming any whitespace
			[e.target.name]: e.target.value.trim(),
		});
	};

	const handleSubmit = (e) => {
		e.preventDefault();
		console.log(formData);

		axiosInstance.put(`edit-meeting/` + id + '/', {
			date: formData.date,
			time: formData.time,
      book: formData.book,
      location: formData.location,
      link_to_meeting: formData.link_to_meeting,
		})
		.then((res) => {
			navigate('/dashboard');
		});
	};

	const classes = useStyles();
  return (
		<>
		 {userAuth == 'Not found.' &&
          <Navigate to={"/club/"+id}/>
        }
		{userAuth == 'applicant' &&
          <Navigate to={"/club/"+id}/>
        }
		{userAuth == 'member' &&
          <Navigate to={"/club/"+id}/>
        }
		<Template/>
		{userAuth == 'owner' &&
		<Container component="main" maxWidth="sm">
			<CssBaseline />
			<div className={classes.paper}>
				<EditIcon className={classes.avatar}></EditIcon>
				<Title2 >Edit Meeting</Title2>
				<Parragraph>Easily edit your meeting here! everyone will se the changes</Parragraph>
				<form className={classes.form} noValidate>
					<Grid container spacing={2}>
						<Grid item xs={12}>
						<TextField
								variant="outlined"
								required
								fullWidth
								id="date"
								label="Date"
								name="date"
								autoComplete="date"
								value={formData.date}
								onChange={handleChange}
							/>
						</Grid>
						<Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								id="time"
								label="Time"
								name="time"
								autoComplete="time"
								value={formData.time}
								onChange={handleChange}
							/>
						</Grid>
						<Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								id="book"
								label="Book"
								name="book"
								autoComplete="book"
								value={formData.book}
								onChange={handleChange}
							/>
						</Grid>
            <Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								id="location"
								label="Meeting Location"
								name="location"
								autoComplete="location"
								value={formData.location}
								onChange={handleChange}
							/>
						</Grid>
            <Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								id="link_to_meeting"
								label="link_to_meeting"
								name="link_to_meeting"
								autoComplete="link_to_meeting"
								value={formData.link_to_meeting}
								onChange={handleChange}
							/>
						</Grid>
					</Grid>
					<Button
						type="submit"
						fullWidth
						variant="contained"
						color="primary"
						className={classes.submit}
						onClick={handleSubmit}
						style={{backgroundColor: '#643513',}}
					>
						confirm
					</Button>
				</form>
			</div>
		</Container>
		}
		</>
	);}
