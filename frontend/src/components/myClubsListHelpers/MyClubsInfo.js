import React, { useState, useEffect } from "react";
import { makeStyles, Card, CardActionArea, CardContent, Typography, CardActions, Button } from "@material-ui/core";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../../axios";

const useStyles = makeStyles((theme) => ({
    card:{
        marginBottom:theme.spacing(3)
    },
}));


const MyClubsInfo = (props) => {

    const navigate = useNavigate();
    const { clubs } = props;
    const classes = useStyles();

    console.log(clubs);
    //need to clubs
    

    if (!clubs || clubs.length === 0) return <p> Can not find any clubs, sorry</p>;
    return (
        <React.Fragment>
            {clubs.map((club) => {

            const [data, setData] = useState({ user: [] });

            useEffect(() =>  {
                axiosInstance.get('current-user').then((res) => {
                    setData({ user: res.data });
                });
            }, [setData]);


            const handleGoToClub = (e) => {
                navigate('/club/'+ club.id);
            }

            return ( <Card item key={club.id} className={classes.card} >
                <CardActionArea>
                    <CardContent onClick={handleGoToClub}>
                        <Typography gutterBottom variant="h5" style={{color: '#23180a'}} > {club.name} </Typography>
                        <Typography variant="body2"> Members: {club.members_capacity} </Typography>
                    </CardContent>
                </CardActionArea>
                <CardActions>
                    <Button variant="outlined" size="small"  onClick={handleGoToClub}>Info </Button>
                </CardActions>
            </Card>
            );
            })}
        </React.Fragment>
    );
};


export default MyClubsInfo;