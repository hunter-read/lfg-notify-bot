#!/usr/bin/env bash
database=$1
date=$2
if [[ -z $database ]]; then
    echo -n "Enter database location: "
    read database
fi

where=""
start=$((($(date +%s)-$(date +%s --date "2020-11-01"))/(3600*24)))
if [[ "$2" ]]; then
    start=$((($(date +%s)-$(date +%s --date "$2"))/(3600*24)))
    where="WHERE date_created > '$2'"
    sql_and="AND date_created > '$2'"
else
    date="2020-11-01"
fi

results=($(
sqlite3 -batch $database <<EOF
SELECT count(id) FROM user;
SELECT count(id) FROM post $where;
SELECT sum(timezone is not null), sum(day is not null), sum(nsfw = -1), sum(nsfw = 0), sum(nsfw = 1), sum(flair <> 3), sum(keyword is not null), 
 sum(online = 1), sum(online = 0), sum(online = -1), sum(play_by_post = -1), sum(play_by_post = 0), sum(play_by_post = 1), sum(one_shot = -1), sum(one_shot = 0), sum(one_shot = 1),
 sum(lgbtq & 1 > 0), sum(lgbtq & 4 > 0), sum(lgbtq & 2 > 0), sum(lgbtq & 8 > 0),
 sum(vtt & 2 > 0), sum(vtt & 8 > 0), sum(vtt & 4 > 0), sum(vtt & 16 > 0), sum(vtt & 64 > 0), sum(vtt & 32 > 0), sum(vtt & 1 > 0) FROM user;
SELECT sum(game like '%5E%'), sum(game like '%4E%'), sum(game like '%3.5%'), sum(game like '%ADND%'), sum(game like '%PF2E%'), sum(game like '%PF1E%'), sum(game like '%COC%'), sum(game like '%WOD%'), 
 sum(game like '%SWRPG%'), sum(game like '%CYBERPUNK%'), sum(game like '%40K%'), sum(game like '%MOTW%'), sum(game like '%FATE%'), sum(game like '%GURPS%'), sum(game like '%STARFINDER%'), 
 sum(game like '%BITD%'), sum(game like '%COFD%'), sum(game like '%MM3%'), sum(game like '%SWN%'), sum(game like '%SWADE%'), sum(game like '%3E%'), sum(game like '%SR6%'), sum(game like '%SR5%'), 
 sum(game like '%SR4%'), sum(game like '%SR3%'), sum(game like '%DND2E%'), sum(game like '%ODND%'), sum(game like '%BRP%'), sum(game like '%BX%'), sum(game like '%DLC%'), sum(game like '%DLR%'), 
 sum(game like '%DCC%'), sum(game like '%DW%'), sum(game like '%EARTHDAWN%'), sum(game like '%FEAST%'), sum(game like '%FWS%'), sum(game like '%L5R%'), sum(game like '%MCC%'), sum(game like '%NUMENERA%'), 
 sum(game like '%SWD%'), sum(game like '%FLEXIBLE%'), sum(game like '%1DND%') FROM user;
SELECT count(id) FROM post $where GROUP BY nsfw ORDER BY nsfw;
SELECT count(id) FROM post WHERE flair IN ('GM and player(s) wanted', 'Player(s) wanted', 'GM wanted') $sql_and GROUP BY flair ORDER BY flair;
SELECT sum(day like '%MONDAY%'),sum(day like '%TUESDAY%'),sum(day like '%WEDNESDAY%'),sum(day like '%THURSDAY%'),sum(day like '%FRIDAY%'),sum(day like '%SATURDAY%'),sum(day like '%SUNDAY%'),sum(day is null) FROM post $where;
SELECT sum(game like '%5E%'), sum(game like '%4E%'), sum(game like '%3.5%'), sum(game like '%ADND%'), sum(game like '%PF2E%'), sum(game like '%PF1E%'), sum(game like '%COC%'), sum(game like '%WOD%'), 
 sum(game like '%SWRPG%'), sum(game like '%CYBERPUNK%'), sum(game like '%40K%'), sum(game like '%MOTW%'), sum(game like '%FATE%'), sum(game like '%GURPS%'), sum(game like '%STARFINDER%'), 
 sum(game like '%BITD%'), sum(game like '%COFD%'), sum(game like '%MM3%'), sum(game like '%SWN%'), sum(game like '%SWADE%'), sum(game like '%3E%'), sum(game like '%SR6%'), sum(game like '%SR5%'), 
 sum(game like '%SR4%'), sum(game like '%SR3%'), sum(game like '%DND2E%'), sum(game like '%ODND%'), sum(game like '%BRP%'), sum(game like '%BX%'), sum(game like '%DLC%'), sum(game like '%DLR%'), 
 sum(game like '%DCC%'), sum(game like '%DW%'), sum(game like '%EARTHDAWN%'), sum(game like '%FEAST%'), sum(game like '%FWS%'), sum(game like '%L5R%'), sum(game like '%MCC%'), sum(game like '%NUMENERA%'), sum(game like '%SWD%'), sum(game like '%FLEXIBLE%') FROM post $where;
SELECT sum(timezone like '%GMT-4%'), sum(timezone like '%GMT-5%'), sum(timezone like '%GMT-6%'), sum(timezone like '%GMT-7%'), sum(timezone like '%GMT-8%') FROM post $where;
SELECT sum(timezone like '%GMT-1%' and timezone not like '%GMT-10%'), sum(timezone like '%GMT+0%'), sum(timezone like '%GMT+1%' and timezone not like '%GMT+10%'  and timezone not like '%GMT+11%'), sum(timezone like '%GMT+2%'), sum(timezone like '%GMT+3%') FROM post $where;
SELECT sum(timezone like '%GMT+8%'), sum(timezone like '%GMT+9:30%'), sum(timezone like '%GMT+10%' and timezone not like '%GMT+10:%'), sum(timezone like '%GMT+10:30%'), sum(timezone like '%GMT+11%'), sum(timezone is null) FROM post $where;
SELECT sum(online = 1), sum(online = 0), sum(online = -1) FROM post $where;
SELECT sum(play_by_post = 1) FROM post $where;
SELECT sum(one_shot = 1) FROM post $where;
SELECT sum(lgbtq & 1 > 0), sum(lgbtq & 4 > 0), sum(lgbtq & 2 > 0), sum(lgbtq & 8 > 0) FROM post $where;
SELECT sum(vtt & 1 > 0), sum(vtt & 2 > 0), sum(vtt & 8 > 0), sum(vtt & 4 > 0), sum(vtt & 16 > 0), sum(vtt & 64 > 0), sum(vtt & 32 > 0), sum(vtt & 128 > 0), sum(vtt & 256 > 0), sum(vtt & 512 > 0) FROM post $where;
EOF
))
# echo ${results[*]}
echo "***** User Stats *****"
echo "Active users: ${results[0]}"
filter=(${results[2]//|/ })
echo "Filter Usage: "
echo "  Timezone filter: ${filter[0]}"
echo "  Day filter: ${filter[1]}"
echo "  Flair: ${filter[5]}"
echo "  Keyword: ${filter[6]}"
echo "  Location - Online: ${filter[7]}, Both: ${filter[8]}, Offline: ${filter[9]}"
echo "  NSFW - None: ${filter[2]}, Allowing:  ${filter[3]}, Only: ${filter[4]}"
echo "  Play by Post - Exclude: ${filter[10]}, Allow: ${filter[11]}, Only: ${filter[12]}"
echo "  One Shot - Exclude: ${filter[13]}, Allow: ${filter[14]}, Only: ${filter[15]}"
echo "  Identity: "
echo "    LGBTQ+: ${filter[16]}"
echo "    PoC: ${filter[17]}"
echo "    Fem: ${filter[18]}"
echo "    Accessible: ${filter[19]}"
echo "  VTT: "
echo "    Roll20: ${filter[26]}"
echo "    Fantasy Grounds: ${filter[20]}"
echo "    Foundry: ${filter[21]}"
echo "    Tabletop Sim: ${filter[22]}"
echo "    Astral: ${filter[23]}"
echo "    TaleSpire: ${filter[24]}"
echo "    TablePlop: ${filter[25]}"

echo "Game Stats: "
game=(${results[3]//|/ })
echo "  Flexible / Other: ${game[40]}"
echo "  D&D:"
echo "    5e: ${game[0]}, 4e: ${game[1]}, 3.5: ${game[2]}, 3e: ${game[20]}, ADND: ${game[3]}, DND2e: ${game[25]}, ODND: ${game[26]}, 1DND: ${game[41]}"
echo "  Pathfinder: "
echo "    PF2e: ${game[4]}, PF1e: ${game[5]}"
echo "  Others (Grouped alphabetically):"
echo "    40K: ${game[10]}"
echo "    BitD: ${game[15]}, BRP: ${game[27]}, BX: ${game[28]}"
echo "    CoC: ${game[6]}, CofD: ${game[16]}, Cyberpunk: ${game[9]}"
echo "    DCC: ${game[31]}, DLC: ${game[29]}, DLR: ${game[30]}, DW: ${game[32]}"
echo "    Earthdawn: ${game[33]}"
echo "    Fate: ${game[12]}, Feast: ${game[34]}, FWS: ${game[35]}"
echo "    GURPS: ${game[13]}"
echo "    L5R: ${game[36]}"
echo "    MCC: ${game[37]}, MM3: ${game[17]}, MotW: ${game[11]}"
echo "    Numenera: ${game[38]}"
echo "    SR6: ${game[21]}, SR5: ${game[22]}, SR4: ${game[23]}, SR3: ${game[24]}"
echo "    Starfinder: ${game[14]}, SWADE: ${game[19]}, SWD: ${game[39]}, SWN: ${game[18]}, SWRPG: ${game[8]}"
echo "    WoD: ${game[7]}"
echo
echo "***** Post Stats (Since $date) *****"
total=${results[1]}
echo "Total submissions: $total"
avg=$(echo $total / $start | bc)
echo "Avg submissions/day: $avg"
echo "SFW: ${results[4]}, NSFW: ${results[5]}"
online=(${results[14]//|/ })
echo "Online: ${online[0]}, Both: ${online[1]}, Offline: ${online[2]}"
echo "Play by Post: ${results[15]}"
echo "One-Shot: ${results[16]}"
echo "Flair stats:"
echo "  Player(s) wanted: ${results[8]}"
echo "  GM and player(s) wanted: ${results[6]}"
echo "  GM wanted: ${results[7]}"
identity=(${results[17]//|/ })
echo "Identity: "
echo "  LGBTQ+: ${identity[0]}"
echo "  PoC: ${identity[1]}"
echo "  Fem: ${identity[2]}"
echo "  Accessible: ${identity[3]}"
vtt=(${results[18]//|/ })
echo "VTT: "
echo "  Roll20: ${vtt[0]}"
echo "  Fantasy Grounds: ${vtt[1]}"
echo "  Foundry: ${vtt[2]}"
echo "  Tabletop Sim: ${vtt[3]}"
echo "  Astral: ${vtt[4]}"
echo "  TaleSpire: ${vtt[5]}"
echo "  TablePlop: ${vtt[6]}"
echo "  One More Multiverse: ${vtt[7]}"
echo "  Owlbear Rodeo: ${vtt[8]}"
echo "  Above VTT: ${vtt[9]}"
game=(${results[10]//|/ })
echo "Games stats:"
echo "  Flexible / Other: ${game[40]}"
echo "  D&D:"
echo "    5e: ${game[0]}, 4e: ${game[1]}, 3.5: ${game[2]}, 3e: ${game[20]}, ADND: ${game[3]}, DND2e: ${game[25]}, ODND: ${game[26]}"
echo "  Pathfinder: "
echo "    PF2e: ${game[4]}, PF1e: ${game[5]}"
echo "  Others (Grouped alphabetically):"
echo "    40K: ${game[10]}"
echo "    BitD: ${game[15]}, BRP: ${game[27]}, BX: ${game[28]}"
echo "    CoC: ${game[6]}, CofD: ${game[16]}, Cyberpunk: ${game[9]}"
echo "    DCC: ${game[31]}, DLC: ${game[29]}, DLR: ${game[30]}, DW: ${game[32]}"
echo "    Earthdawn: ${game[33]}"
echo "    Fate: ${game[12]}, Feast: ${game[34]}, FWS: ${game[35]}"
echo "    GURPS: ${game[13]}"
echo "    L5R: ${game[36]}"
echo "    MCC: ${game[37]}, MM3: ${game[17]}, MotW: ${game[11]}"
echo "    Numenera: ${game[38]}"
echo "    SR6: ${game[21]}, SR5: ${game[22]}, SR4: ${game[23]}, SR3: ${game[24]}"
echo "    Starfinder: ${game[14]}, SWADE: ${game[19]}, SWD: ${game[39]}, SWN: ${game[18]}, SWRPG: ${game[8]}"
echo "    WoD: ${game[7]}"
echo "Day stats:"
days=(${results[9]//|/ })
echo "  Monday: ${days[0]}"
echo "  Tuesday: ${days[1]}"
echo "  Wednesday: ${days[2]}"
echo "  Thursday: ${days[3]}"
echo "  Friday: ${days[4]}"
echo "  Saturday: ${days[5]}"
echo "  Sunday: ${days[6]}"
echo "  Unknown: ${days[7]}"
echo "Timezone stats:"
us=(${results[11]//|/ })
eu=(${results[12]//|/ })
au=(${results[13]//|/ })
echo "  North America:: GMT-4: ${us[0]}, GMT-5: ${us[1]}, GMT-6: ${us[2]}, GMT-7: ${us[3]}, GMT-8: ${us[4]}"
echo "  Europe::        GMT-1: ${eu[0]}, GMT+0: ${eu[1]}, GMT+1: ${eu[2]}, GMT+2: ${eu[3]}, GMT+3: ${eu[4]}"
echo "  Australia::     GMT+8: ${au[0]}, GMT+9.5: ${au[1]}, GMT+10: ${au[2]}, GMT+10.5: ${au[3]}, GMT+11: ${au[4]}"
echo "  No timezone::   ${au[5]}"