import React, { useState, useEffect } from "react";
import { makeStyles, Container, Card, CardActionArea, CardMedia, CardContent, Typography, CardActions, Button } from "@material-ui/core";
import { useNavigate, useParams } from "react-router-dom";
import axiosInstance from '../../axios';

import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import Parragraph2 from '../clubDisplayHelpers/Parragraph2'

const useStyles = makeStyles((theme) => ({
    card:{
        marginBottom:theme.spacing(5)
    },
}));



const ApplicantInfo = (props) => {

    const navigate = useNavigate();
    const { applicants } = props;
    const classes = useStyles();


    const { id } = useParams();
    const [data, setData] = useState({ clubs: [] });

    useEffect(() =>  {
        axiosInstance.get('club-detail/'+id).then((res) => {
          setData({ clubs: res.data });
          console.log(res.data);
        });
    }, [setData]);

    if (!applicants || applicants.length === 0) return <p> No applications made yet!</p>;
    return (
    <React.Fragment>
        {applicants.map((applicant) => {
            console.log(applicant.id)
            console.log(applicant.user)
            console.log(data.club.name)

        
            const handleAcceptAplicant = (e) => {
                axiosInstance.put('accept-user/'+ applicant.id +'/' , {
                    rank: 'member',
                    club: data.club.name,
                    //find the pk values for both
                    user: applicant.user,
                })
                .then((res) => {
                    navigate('/club/'+ data.club.id);
                })
            };

            return ( <ListItem
                key={applicant.user}
                  secondaryAction={
                      <Button variant="outlined" size="small" onClick={handleAcceptAplicant} >Accept</Button>
                  }
                  disablePadding
                >
                  <ListItemButton dense>
                
                    <Parragraph2>
                    {applicant.user}
                    </Parragraph2>
                  </ListItemButton>
                </ListItem>)
                })}
    </React.Fragment>
    );
};

export default ApplicantInfo;
