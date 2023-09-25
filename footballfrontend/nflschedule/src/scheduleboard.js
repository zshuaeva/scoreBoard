import React, { useEffect, useState } from 'react';
import dotenv from 'dotenv';
dotenv.config();

const apiKey = process.env.REACT_APP_RAPIDAPI_KEY;

function ScheduleBoard() {
  const [scheduleData, setScheduleData] = useState([]);
  const [selectedDate, setSelectedDate] = useState('2023-01-01');
  const [totalGames, setTotalGames] = useState();

  const fetchData = async () => {
    const url = `https://api-american-football.p.rapidapi.com/games?date=${selectedDate}&league=1`;
    const options = {
      method: 'GET',
      headers: {
        'X-RapidAPI-Key': apiKey,
        'X-RapidAPI-Host': 'api-american-football.p.rapidapi.com'
      }
    };

    try {
      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error(`Failed to fetch NFL game data. Status Code: ${response.status}`);
      }
      const data = await response.json();
      setScheduleData(data);
      setTotalGames(data.results);

      console.log('Fetched data:', data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    console.log('Selected Date:', selectedDate);
  }, [selectedDate]);

  return (
    <div>
      <input
        type="date"
        value={selectedDate}
        onChange={(e) => setSelectedDate(e.target.value)}
      />
      <div className='total-games'>
        Games today: {totalGames}
      </div>

      <div className='fetch-button'>
        <button onClick={fetchData}>Get Games</button>
      </div>

      {scheduleData.response && scheduleData.response.length > 0 ? (
        <ul>
          {scheduleData.response.map((current, index) => (
    <li key={index}>
    <img className="team-logos" src={current.teams.home.logo} alt={`${current.teams.home.name} Logo`} />
    @
    <img className="team-logos" src={current.teams.away.logo} alt={`${current.teams.away.name} Logo`} />
    | {current.game.date.time}
  </li>
          ))}
        </ul>
      ) : (
        <p>No games found for the selected date.</p>
      )}
    </div>
  );
}

export default ScheduleBoard;
