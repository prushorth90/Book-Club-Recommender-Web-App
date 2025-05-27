import React, { useState, useEffect } from 'react';
import axiosInstance from '../axios';
import { useNavigate, useParams, Navigate} from 'react-router-dom';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import Navbar from './templateHelpers/Navbar';

const useStyles = makeStyles((theme) => ({
	paper: {
		marginTop: theme.spacing(6),
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

export default function CreatePost() {

    const { id } = useParams();
	const navigate = useNavigate();

	//get information from user, club and user auth

	const [user, setData] = useState({});
	const [clubData, setClubData] = useState({});
	const [userAuth, setUserAuth] = useState(null);

	useEffect(() => {
		axiosInstance.get('current-user/').then((res) => {
		  setData(res.data);
		  console.log(res.data);
		});
	  }, [setData]);

	useEffect(() => {
		axiosInstance.get('club-detail/'+id+'/').then((res) => {
			setClubData(res.data);
			console.log(res.data);
		});
	}, [setClubData]);

	useEffect(() => {
		axiosInstance.get('user-auth-detail/' + id + '/')
		.then((response) => {
		  setUserAuth(response.data.rank);
		  })
		.catch((e) => {
		  setUserAuth(e.response.data.detail);
		});
  
	  }, [setUserAuth]);


	const initialFormData = Object.freeze({text: ''});

	const [formData, updateFormData] = useState(initialFormData);

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

		axiosInstance
			.post(`/create-post/`+id, {
                //fix the name
                author: user.username,
                text: formData.text,
                club: clubData.name,
			})
			.then((res) => {
				navigate('/club/'+id);
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
		<Navbar/>
		{userAuth != null &&
		<Container component="main" maxWidth="xs">
			<CssBaseline />
			<div className={classes.paper}>
				<Typography component="h1" variant="h5">
					Create a post
				</Typography>
				<form className={classes.form} noValidate>
					<Grid container spacing={2}>
                        <Grid item xs={12}>
							<TextField
								variant="outlined"
								fullWidth
                                multiline
                                rows={4}
								id="text"
								label="text"
								name="text"
								autoComplete="text"
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
					>
						Create Post
					</Button>
				</form>
			</div>
		</Container>
		}
		</>
	);
}