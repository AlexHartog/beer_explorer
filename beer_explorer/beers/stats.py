from .models import BeerCheckin
import pandas as pd
from pprint import pprint
from django.db.models import F, Q


class UserStats:
    def __init__(self):
        # Load checkins
        beer_checkins = BeerCheckin.objects.prefetch_related("joint_checkin").all()

        data = []
        for checkin in beer_checkins:
            joint_checkin_users = list(
                checkin.joint_checkin.all().values_list("name", flat=True)
            )

            data.append(
                {
                    "user_name": checkin.user.name,
                    "date": checkin.date,
                    "in_bar": checkin.in_bar,
                    "beer_id": checkin.beer.id,
                    "joint_checkin": ", ".join(joint_checkin_users),
                }
            )

        beer_checkin_df = pd.DataFrame(data)
        beer_checkin_df["week_number"] = (
            pd.to_datetime(beer_checkin_df["date"]).dt.isocalendar().week
        )

        # Find first beer checkins
        pprint(beer_checkin_df)
        first_beer_checkins = (
            beer_checkin_df.loc[:, ["beer_id", "date"]]
            .drop_duplicates()
            .reset_index(drop=True)
        )
        # Merge with checkins
        self.valid_beer_checkins = first_beer_checkins.merge(
            beer_checkin_df, on=["beer_id", "date"]
        )

    def get_unique_beers_per_user(self):
        return (
            self.valid_beer_checkins.groupby("user_name")
            .size()
            .reset_index(name="points_unique")
        )

    def get_unique_beer_in_bar_per_user(self):
        return (
            self.valid_beer_checkins[self.valid_beer_checkins["in_bar"]]
            .groupby("user_name")
            .size()
            .reset_index(name="points_bars")
        )

    def get_unique_weeks_per_user(self):
        return (
            self.valid_beer_checkins.groupby("user_name")["week_number"]
            .nunique()
            .reset_index(name="points_weeks")
        )

    def get_joint_checkins_per_user(self):
        return (
            self.valid_beer_checkins[
                self.valid_beer_checkins["joint_checkin"].astype(bool)
            ]
            .groupby("user_name")
            .size()
            .reset_index(name="points_joint_checkin")
        )

    def get_stats(self):
        points = (
            self.get_unique_beers_per_user()
            .merge(
                self.get_unique_beer_in_bar_per_user(),
                on=["user_name"],
                how="left",
            )
            .merge(
                self.get_unique_weeks_per_user(),
                on=["user_name"],
                how="left",
            )
            .merge(
                self.get_joint_checkins_per_user(),
                on=["user_name"],
                how="left",
            )
            .fillna(0)
        )

        points["total_points"] = (
            points["points_unique"]
            + points["points_bars"]
            + points["points_joint_checkin"]
            + points["points_weeks"] * 5
        )

        return points.to_dict("records")
