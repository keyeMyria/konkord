var CONSTANTS = {};

//language
if( $('.js-language-wrapp').data('language') == 'ru' ){
	CONSTANTS.siteLanguage = '';
}else if ($('.js-language-wrapp').data('language') == 'uk'){
	CONSTANTS.siteLanguage = '/uk';
} 

//solutions
CONSTANTS.minHugeScreen = 1601;
CONSTANTS.maxLargeScreen = 1600;
CONSTANTS.minLargeScreen = 1200;
CONSTANTS.maxMediumScreen = 1199;
CONSTANTS.minMediumScreen = 992;
CONSTANTS.maxSmallScreen = 991;
CONSTANTS.minSmallScreen = 768;
CONSTANTS.maxExtrasmallScreen = 767;

CONSTANTS.pageType = $('body').data('page-type');