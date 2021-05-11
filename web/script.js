// Looking for the v1.5 template?
// https://codepen.io/pen?template=GVoaNe

const App = {
  template: '#app-template',
  data: () => ({
    selectedGames: [],
    games: [
      {label: 'Blades in the Dark', value: 'BitD'},
      {label: 'Basic Role-Playing', value: 'BRP'},
      {label: 'Call of Cthulhu', value: 'CoC'},
      {label: 'Chronicles of Darkness', value: 'CofD'},
      {label: 'Cyberpunk 2020', value: 'Cyberpunk'},
      {label: 'Deadlands Classics', value: 'DLC'},
      {label: 'Deadlands Reloaded', value: 'DLR'},
      {label: 'Dungeon Crawl Classics', value: 'DCC'},
      {label: 'Dungeon World', value: 'DW'},
      {label: 'D&D Original Edition', value: 'ODND'},
      {label: 'D&D Advanced', value: 'ADND'},
      {label: 'D&D Basic/Expert', value: 'BX'},
      {label: 'D&D 2nd Edition', value: 'DND2e'},
      {label: 'D&D 3rd Edition', value: '3e'},
      {label: 'D&D 3.5 Edition', value: '3.5'},
      {label: 'D&D 4th Edition', value: '4e'},
      {label: 'D&D 5th Edition', value: '5e'},
      {label: 'Earthdawn', value: 'Earthdawn'},
      {label: 'Fate Core', value: 'Fate'},
      {label: 'Feast of Legends', value: 'Feast'},
      {label: 'Fellowship', value: 'FWS'},
      {label: 'GURPS', value: 'GURPS'},
      {label: 'Legend of the Five Rings', value: 'L5R'},
      {label: 'Monster Crawl Classics', value: 'MCC'},
      {label: 'Monster of the Week', value: 'MotW'},
      {label: 'Mutants & Masterminds 3rd Edition', value: 'MM3'},
      {label: 'Numenera', value: 'Numenera'},
      {label: 'Pathfinder 1st Edition', value: 'PF1e'},
      {label: 'Pathfinder 2nd Edition', value: 'PF2e'},
      {label: 'Savage Worlds Adventure Edition', value: 'SWADE'},
      {label: 'Savage Worlds Deluxe', value: 'SWD'},
      {label: 'Shadowrun 3rd Edition', value: 'SR3'},
      {label: 'Shadowrun 4th Edition', value: 'SR4'},
      {label: 'Shadowrun 5th Edition', value: 'SR5'},
      {label: 'Shadowrun 6th Edition', value: 'SR6'},
      {label: 'Starfinder', value: 'Starfinder'},
      {label: 'Star Wars RPG', value: 'SWRPG'},
      {label: 'Stars Without Numbers', value: 'SWN'},
      {label: 'Warhammer 40K', value: '40K'},
      {label: 'World of Darkness', value: 'WoD'},
    ],
    selectedDays: [],
    days: [
      {label: 'Monday', value: 'mon'},
      {label: 'Tuesday', value: 'tue'},
      {label: 'Wednesday', value: 'wed'},
      {label: 'Thursday', value: 'thu'},
      {label: 'Friday', value: 'fri'},
      {label: 'Saturday', value: 'sat'},
      {label: 'Sunday', value: 'sun'},
    ],
    selectedTimezone: [],
    timezones: [
      'UTC-11', 
      'UTC-10', 
      'UTC-9', 
      'UTC-8', 
      'UTC-7', 
      'UTC-6', 
      'UTC-5', 
      'UTC-4',
      'UTC-3', 
      'UTC-2', 
      'UTC-1', 
      'UTC',
      'UTC+1', 
      'UTC+2', 
      'UTC+3', 
      'UTC+4',
      'UTC+5',
      'UTC+6',
      'UTC+7',
      'UTC+8',
      'UTC+9',
      'UTC+10',
      'UTC+11',
      'UTC+12'
    ],
    selectedKeywords: [],
    keywords: [],
    selectedFlair: ['gmplw', 'plw'],
    flairs: [
      {label: 'GM and player(s) wanted', value: 'gmplw'},
      {label: 'Player(s) wanted', value: 'plw'},
      {label: 'GM wanted', value: 'gmw'}
    ],
    selectedLocation: '',
    locations: [
      {label: 'Online Only', value: ''},
      {label: 'Both Online and Offline', value: 'off'},
      {label: 'Offline Only', value: '=off'}
    ],
    selectedNSFW: '',
    nsfw: [
      {label: 'Exclude all NSFW', value: ''},
      {label: 'Include NSFW', value: 'nsfw'},
      {label: 'Only NSFW', value: '=nsfw'}
    ],
    selectedAge: '',
    ages: [
      {label: 'Any', value: ''},
      {label: 'No age limits', value: 'anyage'},
      {label: '18+', value: '18+'},
      {label: '21+', value: '21+'},
    ],
    selectedPbp: '',
    pbp: [
      {label: 'Include Play-by-Post', value: ''},
      {label: 'Exclude all Play-by-Post', value: '-pbp'},
      {label: 'Only Play-by-Post', value: 'pbp'},
    ],
    selectedOneShot: '',
    oneShot: [
      {label: 'Include One-shots', value: ''},
      {label: 'Exclude all One-shots', value: '-oneshot'},
      {label: 'Only One-shots', value: 'oneshot'},
    ],
    selectedVtt: [],
    vtt: [
      {label: 'Roll20', value: 'roll20'},
      {label: 'Fantasy Grounds', value: 'fg'},
      {label: 'Tabletop Simulator', value: 'tts'},
      {label: 'Foundry VTT', value: 'foundry'},
    ],
    selectedIdentity: [],
    identities: [
      {label: 'LGBTQ+', value: 'lgbtq'},
      {label: 'Feminine or Woman', value: 'fem'},
      {label: 'People of Color', value: 'poc'},
      {label: 'Accessible', value: 'accessible'},
    ],
    sendToReddit: function () {
      url = 'https://www.reddit.com/message/compose/?to=LFG_Notify_Bot&subject=Subscribe&message='
      message =`${this.selectedGames.join(' ')}  \n`;
      if (this.selectedTimezone) { message += `${this.selectedTimezone.join(' ')}  \n`};
      if (this.selectedDays) { message += `${this.selectedDays.join(' ')}  \n`};
      if (this.selectedFlair) { message += `${this.selectedFlair.join(' ')}  \n`};
      if (this.selectedLocation) { message += `${this.selectedLocation}  \n`};
      if (this.selectedVtt) { message += `${this.selectedVtt.join(' ')}  \n`};
      if (this.selectedNSFW) { message += `${this.selectedNSFW}  \n`};
      if (this.selectedAge) { message += `${this.selectedAge}  \n`};
      if (this.selectedPbp) { message += `${this.selectedPbp}  \n`};
      if (this.selectedOneShot) { message += `${this.selectedOneShot}  \n`};
      if (this.selectedIdentity) { message += `${this.selectedIdentity.join(' ')}  \n`};
      if (this.selectedKeywords) { message += `${this.selectedKeywords.forEach(item => `[${item}]`).join(' ')}  \n`};
      window.location.href = (url + encodeURI(message));
    }
    
  })
}

new Vue({
  vuetify: new Vuetify({
    theme: { dark: true },
  }),
  render: h => h(App)
}).$mount('#app')