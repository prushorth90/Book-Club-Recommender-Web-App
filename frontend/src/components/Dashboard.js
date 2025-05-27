import React, { useEffect, useState } from "react";
import { makeStyles, Container, Grid} from "@material-ui/core";
import axiosInstance from '../axios';

import ClubInfo from "./ClubInfo";
import ClubInfoLoadingComponent from "./ClubInfoLoading";
import Template from './Template';
import Title from './clubDisplayHelpers/Title';
import Parragraph from './clubDisplayHelpers/Parragraph';
import UserRecommenderList from './userRecommenderHelpers/UserRecommenderList';


const useStyles = makeStyles((theme) => ({
  container:{
      paddingTop: theme.spacing(10),
      overflow:"auto",
      maxHeight: 800,
      backgroundColor: '#f5f5f5',
      minWidth: '100%',
      minHeight: '100%',
  }
}));

const Dashboard = () => {

  const ClubInfoLoading = ClubInfoLoadingComponent(ClubInfo);
  const [appState, setAppState] = useState({
      loading: true,
      clubs: null,
  });

  useEffect(() => {
      axiosInstance.get('other-clubs-list/').then((clubs) => {
                  const allClubs = clubs.data
                  setAppState({ loading: false, clubs: allClubs });
              });
  }, [setAppState]);


  const classes = useStyles();
  return (
    <Container className ={classes.container}>
        <Template/>
        <Grid container>
            <Grid item sm={1} >
            </Grid>
            <Grid item sm={6} >
                <Title>Your Dashboard</Title>

                <Parragraph>This is a list of all the clubs you can apply for</Parragraph>
                <ClubInfoLoading isLoading={appState.loading} clubs={appState.clubs} />
            </Grid>
            <Grid item sm={4} >
                <UserRecommenderList/>
            </Grid>
        </Grid>
    </Container>
  )
};

export default Dashboard;