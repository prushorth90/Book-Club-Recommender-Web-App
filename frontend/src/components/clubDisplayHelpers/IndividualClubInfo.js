import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import axiosInstance from "../../axios";


export default function Club() {
    const { id } = useParams();
    
    const [data, setData] = useState({ clubs: [] });

    useEffect(() =>  {
        axiosInstance.get('club-detail/'+id).then((res) => {
          setData({ clubs: res.data });
          console.log(res.data);
        });
    }, [setData]);

    return (
      <div>
                  <p> Club Name: {data.clubs.name} </p>
                  <p> Club Description: {data.clubs.description} </p>
                  <p> Members: { '' + data.clubs.members_capacity } </p>
      </div>
    );
}
