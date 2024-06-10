# scraper/live.py

from dingoapp.models import Team, Match

def parseLiveSoup(soup):
    wrapperDiv = soup.find("div", {"id": "spieltagsbox"})
    del soup

    categories = [category.find("h2").find("a")["title"] for category in wrapperDiv.find_all("div", {"class": "kategorie"})]
    categoryMatchesRaw = wrapperDiv.find_all("tbody")
    del wrapperDiv

    result = {}
    for i, categoryMatchRaw in enumerate(categoryMatchesRaw):
        matchesRaw = categoryMatchRaw.find_all("tr")
        matches = []
        for matchRaw in matchesRaw:
            id = int(matchRaw["id"])
            cellsRaw = matchRaw.find_all("td")[:5]

            # if match started get scores of teams
            scoreOrTime = cellsRaw[3].text.strip().replace(" ", "").lower()
            matchStarted = True
            homeTeamScore = None
            awayTeamScore = None
            if "pm" in scoreOrTime or "am" in scoreOrTime:
                matchStarted = False

            matchPostponed = False
            if "postponed" in scoreOrTime:
                matchPostponed = True
                matchStarted = False

            if matchStarted and not matchPostponed:
                scoreOrTime = scoreOrTime.replace("ht", "")
                homeTeamScore, awayTeamScore = [int(i) for i in scoreOrTime.split(":")]

            matchFinished = False
            liveInfo: str = cellsRaw[0].text.strip()
            if matchStarted and any(c.isalpha() for c in liveInfo) and liveInfo.lower() != "ht":
                matchFinished = True

            homeTeam, _ = Team.objects.get_or_create(team_name=cellsRaw[2].text.strip().replace("\"", "").replace("'", ""))
            awayTeam, _ = Team.objects.get_or_create(team_name=cellsRaw[4].text.strip().replace("\"", "").replace("'", ""))

            matchInfoObj = {
                "id": id,
                "homeTeam": homeTeam,
                "awayTeam": awayTeam,
            }
            if not matchStarted:
                matchInfoObj["status"] = "Not Started" if not matchPostponed else "Postponed"
            elif matchStarted and not matchFinished:
                matchInfoObj["status"] = "Live" if not matchPostponed else "Postponed"
                matchInfoObj["homeTeamScore"] = homeTeamScore
                matchInfoObj["awayTeamScore"] = awayTeamScore
            else:
                matchInfoObj["status"] = "Finished" if not matchPostponed else "Postponed"
                matchInfoObj["homeTeamScore"] = homeTeamScore
                matchInfoObj["awayTeamScore"] = awayTeamScore

            match, _ = Match.objects.update_or_create(
                id=id,
                defaults={
                    'home_team': homeTeam,
                    'away_team': awayTeam,
                    'match_status': matchInfoObj["status"],
                    'home_score': matchInfoObj.get("homeTeamScore", 0),
                    'away_score': matchInfoObj.get("awayTeamScore", 0),
                    'match_date': matchInfoObj.get("match_date")
                }
            )
            matches.append(matchInfoObj)
        result[categories[i]] = matches

    return result
