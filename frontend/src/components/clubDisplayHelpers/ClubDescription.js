import React, { useState, useEffect } from "react";
import Title from './Title';
import { useParams } from 'react-router-dom';
import axiosInstance from "../../axios";


export default function ClubDescription() {

    // get variable name from the parameters of the url
    const { id } = useParams();
    
    // create an empty set for the club data adnd its set method (setData)
    const [data, setData] = useState({ club: [] });

    useEffect(() =>  {
        axiosInstance.get('club-detail/'+id).then((res) => {
          //assign the the obtained data to the empty set
          setData({ club: res.data });
        });
    }, [setData]);

  return (
    <>
        
        <Title>{data.club.name}</Title>
        <p> Club Description: {data.club.description} </p>
        <p> Members: { '' + data.club.members_capacity } </p>
    </>
  );
}