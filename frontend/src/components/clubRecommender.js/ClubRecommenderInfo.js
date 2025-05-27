import React from "react";
import { makeStyles, Card, CardActionArea, CardMedia, CardContent} from "@material-ui/core";
import Parragraph2 from "../clubDisplayHelpers/Parragraph2";
import Grid from '@mui/material/Grid';

const useStyles = makeStyles((theme) => ({
    card:{
        marginBottom:theme.spacing(1)
    },
}));


const ClubRecommenderInfo = (props) => {

    const { recommendations } = props;
    const classes = useStyles();

    if (!recommendations || recommendations.length === 0) return <p> No recommendations made yet!</p>;
    return (
        <React.Fragment>
    {recommendations.map((recommendation) => {
    return ( <Card item key={recommendation.isbn} className={classes.card}>
        <CardActionArea>
            <Grid sx={{
                display: 'flex',
                flexDirection: 'row',
            }}>
                <CardMedia
                style={{ width: '6%', height:  '6%'}}
                component="img"
                image={recommendation.image_url}
                />

                <CardContent style={{marginLeft: '8px'}}>
                    <Parragraph2> {recommendation.title} </Parragraph2>
                </CardContent>
             </Grid>
        </CardActionArea>
    </Card>
    );
    })}
    </React.Fragment>
    );
};

export default ClubRecommenderInfo;