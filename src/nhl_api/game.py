"""
Module that is used for getting basic information about a game
such as the scoreboard and the box score.
"""

from nhl_api.utils import convert_time
import nhl_api.data
import nhl_api.object


def scoreboard(year, month, day):
    """
        Return the scoreboard information for games matching the parameters
        as a dictionary.
    """
    data = nhl_api.data.get_schedule(year, month, day)
    if not data:
        return data
    parsed = data.json()

    if parsed["games"]:
        games_data = parsed["games"]
        games = {}
        for game in games_data:
            game_id = game['id']
            season = game['season']
            game_type = game['gameType']
            game_date = game['startTimeUTC']

            home_team_id = int(game['homeTeam']['id'])
            home_team_name = game['homeTeam']['name']['default']
            away_team_id = int(game['awayTeam']['id'])
            away_team_name = game['awayTeam']['name']['default']
            try:
                home_score = game['homeTeam']['score']
            except:
                home_score = "0"
            try:
                away_score = game['awayTeam']['score']
            except:
                away_score = "0"

            status = game['gameState']
            status_code = game['gameScheduleState']
            status_abstract_state = game['gameState']
            if (home_score == None) or (away_score == None):
                linescore = "0-0"
            elif int(home_score) > int(away_score):
                linescore = f"{home_score}-{away_score}"
            else:
                linescore = f"{away_score}-{home_score}"

            output = {
                'game_id': game_id,
                'season': season,
                'game_type': game_type,
                'game_date': game_date,
                'home_team_id': home_team_id,
                'home_team_name': home_team_name,
                'away_team_id': away_team_id,
                'away_team_name': away_team_name,
                'home_score': home_score,
                'away_score': away_score,
                'status': status,
                'status_code': status_code,
                'status_abstract_state': status_abstract_state,
                # All the linescore information (goals, sog, periods etc...)
                'linescore': linescore,
            }

            # put this dictionary into the larger dictionary
            games[game_id] = output
        return games
    else:
        return []


class GameScoreboard(object):

    def __init__(self, data):
        # loop through data
        for x in data:
            # set information as correct data type
            try:
                setattr(self, x, int(data[x]))
            except ValueError:
                try:
                    setattr(self, x, float(data[x]))
                except ValueError:
                    # string if not number
                    setattr(self, x, str(data[x]))
            except TypeError:
                obj = nhl_api.object.Object(data[x])
                setattr(self, x, obj)

        # calculate the winning team
        if self.home_score > self.away_score:
            self.w_team = self.home_team_id
            self.l_team = self.away_team_id
        elif self.away_score > self.home_score:
            self.w_team = self.away_team_id
            self.l_team = self.home_team_id

        self.full_date = convert_time(self.game_date).strftime("%Y-%m-%d")
        self.start_time = convert_time(self.game_date).strftime("%I:%M")

    def __str__(self):
        return ('{0.away_team_name} ({0.away_score}) VS '
                '{0.home_team_name} ({0.home_score})').format(self)

    def __repr__(self):
        return self.__str__()


def overview(game_id):
    data = nhl_api.data.get_overview(game_id)
    parsed = data
    # Top level information (General)
    id = parsed['id']
    time_stamp = 0 #parsed['gameData']['game']
    if parsed['gameType'] == 2:
        game_type = "R"
    else:
        debug.log("game type is " + str(parsed['gameType']))
        game_type = "P"

    status = data
    status_code = parsed["gameState"]
    status_abstract_state = parsed["gameState"]
    game_date = parsed['startTimeUTC']

    # Sub level information (Details)
    if parsed["gameState"] == "FUT":
        plays = ""
        linescore = ""
        boxscore = ""
        away_score = "0"
        home_score = "0"
        home_sog = "0"
        away_sog = "0"
    else:
        plays = ""
        linescore = parsed['boxscore']['linescore']
        boxscore = parsed['boxscore']
        away_score = linescore['awayTeam']['score']
        home_score = linescore['homeTeam']['score']
        home_sog = parsed['homeTeam']['sog']
        away_sog = parsed['awayTeam']['sog']

    # Team details
    away_team_id = parsed['awayTeam']['id']
    away_team_name = parsed['awayTeam']['name']['default']
    away_team_abrev = parsed['awayTeam']['abbrev']
    home_team_id = parsed['homeTeam']['id']
    home_team_name = parsed['homeTeam']['name']['default']
    home_team_abrev = parsed['homeTeam']['abbrev']

    # 3 stars (if any available)
    try:
        first_star = parsed['liveData']['decisions']['firstStar']
        second_star = parsed['liveData']['decisions']['secondStar']
        third_star = parsed['liveData']['decisions']['thirdStar']

    except:
        first_star = {}
        second_star = {}
        third_star = {}

    output = {
        'id': id,  # ID of the game
        'time_stamp': time_stamp,  # Last time the data was refreshed (UTC)
        # Type of game ("R" for Regular season, "P" for Post season or playoff)
        'game_type': game_type,
        'status': status,   # Status of the game.
        'status_code': status_code,
        'status_abstract_state': status_abstract_state,
        'game_date': game_date,  # Date and time of the game
        'away_team_id': away_team_id,  # ID of the Away team
        'away_team_name': away_team_name,  # Away team name
        'away_team_abrev': away_team_abrev,  # Away team name abbreviation
        'home_team_id': home_team_id,  # ID of the Home team
        'home_team_name': home_team_name,  # Home team name
        'home_team_abrev': home_team_abrev,  # Home team name abbreviation
        # All the linescore information (goals, sog, periods etc...)
        'linescore': linescore,
        # All the boxscore information (players, onice, team's stats, penalty box etc...)
        'boxscore': boxscore,
        'away_score': away_score,  # Away team goals
        'home_score': home_score,  # Home team goals
        'plays': plays,  # Dictionary of all the plays of the game.
        'first_star': first_star,
        'second_star': second_star,
        'third_star': third_star,
        'inIntermission' : parsed['clock']['inIntermission'],
        'home_sog' : home_sog,
        'away_sog' : away_sog,
    }
    return output


class Overview(object):
    def __init__(self, data):
        # loop through data
        for x in data:
            # set information as correct data type
            try:
                setattr(self, x, int(data[x]))
            except ValueError:
                try:
                    setattr(self, x, float(data[x]))
                except ValueError:
                    # string if not number
                    setattr(self, x, str(data[x]))
            except TypeError:
                obj = nhl_api.object.Object(data[x])
                setattr(self, x, obj)
        
        # calculate the winning team
        if self.home_score > self.away_score:
            self.w_team = self.home_team_id
            self.w_score = self.home_score
            self.l_team = self.away_team_id
            self.l_score = self.away_score
        elif self.away_score > self.home_score:
            self.w_team = self.away_team_id
            self.w_score = self.away_score
            self.l_team = self.home_team_id
            self.l_score = self.home_score
