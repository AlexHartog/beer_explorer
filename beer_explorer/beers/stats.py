from .models import BeerCheckin
import pandas as pd
from pprint import pprint
from django.db.models import F, Q


class UserStats:
    def __init__(self):
        # Load checkins
        beer_checkins = BeerCheckin.objects.all().values(user_name=F("user__name"))

        beer_checkin_df = pd.DataFrame(list(beer_checkins.values()))
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

        pass

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
            .fillna(0)
        )

        points["total_points"] = (
            points["points_unique"] + points["points_bars"] + points["points_weeks"]
        )

        return points.to_dict("records")
