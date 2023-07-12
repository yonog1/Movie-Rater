import { Fragment, useState } from "react";
import { StarRate } from "../../node_modules/@mui/icons-material/index";

const NUMBER_OF_STARS = 5;

export default function MoiveDetails(props) {
    const [highlighted, setHilighted] = useState(-1);

    const highlightStars = (highlited) => (event) => {
        setHilighted(highlited);
    };

    const ratingClicked = (rating) => (event) => {
        fetch(
            `http://localhost:8000/api/movies/${props.movie.id}/rate_movie/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: process.env.REACT_APP_TOKEN,
                },
                body: JSON.stringify({ stars: rating + 1 }),
            }
        )
            .then(() => getDetails())
            .then(() => {
                setHilighted(rating + 1);
            })
            .catch((error) => console.log(error));
    };

    const getDetails = () => {
        fetch(`http://localhost:8000/api/movies/${props.movie.id}/`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: process.env.REACT_APP_TOKEN,
            },
        })
            .then((response) => response.json())
            .then((response) => props.updateMovie(response))
            .catch((error) => console.log(error));

        fetch(`http://localhost:8000/api/movies/user_rating/`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: process.env.REACT_APP_TOKEN,
            },
        })
            .then((response) => response.json())
            .then((response) => console.log(response))
            .catch((error) => console.log(error));
    };

    return (
        <div>
            {props.movie.title ? (
                <div>
                    <h1>{props.movie.title}</h1>
                    <p>{props.movie.description}</p>
                    {/*console.log(props.movie.avg_rating)*/}
                    <Fragment>
                        {[...Array(props.movie.avg_rating)].map(
                            (val, index) => {
                                return (
                                    <Fragment key={index}>
                                        <StarRate style={{ color: "yellow" }} />
                                    </Fragment>
                                );
                            }
                        )}
                        {[
                            ...Array(NUMBER_OF_STARS - props.movie.avg_rating),
                        ].map((val, index) => {
                            return (
                                <Fragment key={index}>
                                    <StarRate style={{ color: "white" }} />
                                </Fragment>
                            );
                        })}
                    </Fragment>
                    ({props.movie.number_of_ratings})
                    <div className="rate-container">
                        <h2>Rate it</h2>
                        {[...Array(NUMBER_OF_STARS)].map((element, index) => {
                            return (
                                <StarRate
                                    cursor="pointer"
                                    sx={{ fontSize: "1.8rem" }}
                                    onMouseEnter={highlightStars(index + 1)}
                                    onMouseLeave={highlightStars(-1)}
                                    onClick={ratingClicked(index)}
                                    key={index}
                                    style={
                                        highlighted > index
                                            ? { color: "yellow" }
                                            : { color: "white" }
                                    }
                                />
                            );
                        })}
                    </div>
                </div>
            ) : (
                <div>{null}</div>
            )}
        </div>
    );
}
