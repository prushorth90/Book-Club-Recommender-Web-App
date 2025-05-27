import React, { useState, useContext } from "react";
import { Button } from "@material-ui/core";
import { Grid } from "@material-ui/core";
import { TextField } from "@material-ui/core";
import { useNavigate } from "react-router-dom";
import CssBaseline from '@material-ui/core/CssBaseline';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import GroupsIcon from '@mui/icons-material/Groups';

import axiosInstance from "../axios";
import Parragraph from "./clubDisplayHelpers/Parragraph";
import Title2 from "./clubDisplayHelpers/Title2";
import AuthContext from "../context/AuthContext";
import Template from "./Template";
import Club from "./Club";

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

export default function CreateClubPage() {
  let {user} = useContext(AuthContext)

  const navigate = useNavigate();
  const initialFormData = Object.freeze ({
    name: '',
    description: '',
    members_capacity: 2,
  });

  const [formData, updateFormData] = useState(initialFormData);

  const handleChange = (e) => {
    if ([e.target.name] == 'name') {
      updateFormData({
              ...formData,
              [e.target.name]: e.target.value.trim(),
      });
    } else {
          updateFormData({
              ...formData,
              [e.target.name]: e.target.value.trim(),
          });
    }
  };
  
  const handleSubmit = async (e) => {
          e.preventDefault();
          await axiosInstance.post('create-club/', {
            name: formData.name,
            description: formData.description,
            members_capacity: formData.members_capacity,
          });
          axiosInstance.post('create-user-auth/', {
            rank: 'owner',
            //find the pk values for both
			club: formData.name,
            user: user.username,
          })
		//   axiosInstance.post('chat-room/', {
		// 	club: Club,
		// 	name:formData.name,
		// 	created_by : user.username,
		// 	members : null,
		// 	timestamp : Date.now(),
        //   })
          .then((res) => {
            navigate('/dashboard');
          })
  };
  const classes = useStyles();

    return (
      <>
		<Template/>
		<Container component="main" maxWidth='sm' margin='100' >
			<CssBaseline />
			
			<div className={classes.paper}>
			
				<GroupsIcon className={classes.avatar}></GroupsIcon>
				<Title2>Create A Club</Title2>
				<Parragraph>Create a Club so you can chat and read with your friends!</Parragraph>
				<form className={classes.form} noValidate>
					<Grid container spacing={2}>
					<Grid item xs={12} align="center">
						<TextField
							variant="outlined"
							required
							fullWidth
							id="name"
							label="Name"
							name="name"
							autoComplete="name"
							onChange={handleChange}
						/>
					</Grid>
					<Grid item xs={12} align="center">
						<TextField
							variant="outlined"
							fullWidth
							multiline
							rows={4}
							id="description"
							label="Description"
							name="description"
							autoComplete="description"
							onChange={handleChange}
										/>
					</Grid>
					<Grid item xs={12} align="center">
						<TextField

							type="number" 
							variant="outlined"
							required
							fullWidth
							id="members_capacity"
							label="Members Capacity"
							name="members_capacity"
							autoComplete="members_capacity"
							onChange={handleChange}
							inputProps={{
							min: 1,
							style: {textAlign: "center"},
							}}
										/>
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
							Create Club
						</Button>
					</Grid>
				</form>
			</div>
		</Container>
		</>
    );
  }