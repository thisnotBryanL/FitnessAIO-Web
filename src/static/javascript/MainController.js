(function () {
    'use strict';

    angular.module('app')
        .controller('mainController', MainController);

    MainController.$inject = ['$localStorage', '$log'];

    function MainController($localStorage, $log) {

        var _kgToPoundRatio = 2.2046226218;
        var _cmToInRatio = 0.39370;
        var _selectedActivity = '';
        var _selectedDeficit = '';
        var _selectedMacroSplit = '';
        var _inputWeight = '';

        var vm = this;

        vm.title = 'ThinkEatLift Calories/Macros!';

        vm.activityOptions = [
            { value: '1.2', name: 'Sedentary', kinoFactor: 13, description: 'only weight traing at the gym and sedentary the rest of the time' },
            { value: '1.35', name: 'Lightly active (fits most people)', kinoFactor: 15, description: 'mostly sedentary, one hour of activity every day + weight training 3-4 times a week' },
            { value: '1.55', name: 'Active', kinoFactor: 15, description: 'walking or cycling every day + weight training 3-4 times a week' },
            { value: '1.75', name: 'Very active', kinoFactor: 16, description: 'manual labour + weight training and sports 4-5 times a week' }
        ];

        vm.deficitOptions = [
            { value: '0.9', name: 'Light Cut (-10%)', proteinKgFactor: 2, goal: 'cut' },
            { value: '0.8', name: 'Normal Cut (-20%)', proteinKgFactor: 2, goal: 'cut' },
            { value: '0.75', name: 'Maximum Cut (-25%)', proteinKgFactor: 2, goal: 'cut' },
            { value: '1.0', name: 'Maintenance', proteinKgFactor: 2, goal: 'maintain' },
            { value: '1.1', name: 'Lean Bulk (+10%)', proteinKgFactor: 2.2, goal: 'lean bulk' },
        ];

        vm.macroSplitOptions = [
            {
                id: 'kb_ggp_f20',
                name: 'Kinobody GGP / Radu / 20% fats',
                fatFactor: 0.2,
            },
            {
                id: 'kb_ggp_f25',
                name: 'Kinobody GGP / Radu / 25% fats (default)',
                fatFactor: 0.25,
                getProteinGrams: function (weight, gender, availableCalories) {
                    return weight * vm.selectedDeficit.proteinKgFactor;
                },
                getFatGrams: function (weight, gender, availableCalories) {
                    return 0.25 * availableCalories / 9;
                },
            },
            {
                id: 'kb_ggp_f30',
                name: 'Kinobody GGP / Radu / 30% fats',
                fatFactor: 0.30

            },
            {
                id: 'kb_afl',
                name: 'Kinobody AFL (p: 35%, f: 30%, c: 35%)',
                fatFactor: 0.30,
                getProteinGrams: function (weight, gender, availableCalories) {
                    return 0.35 * availableCalories / 4;
                },
                getFatGrams: function (weight, gender, availableCalories) {
                    return 0.30 * availableCalories / 9;
                },
                // getCarbGrams: function(weight, gender, availableCalories) {
                //   return 0.35 * availableCalories / 4;
                // },
            },
            {
                id: 'kb_gtp',
                name: 'Kinobody GTP (p: 35%, f: 25%, c: 40%)',
                fatFactor: 0.30,
                getProteinGrams: function (weight, gender, availableCalories) {
                    return 0.35 * availableCalories / 4;
                },
                getFatGrams: function (weight, gender, availableCalories) {
                    return 0.25 * availableCalories / 9;
                },
                // getCarbGrams: function(weight, gender, availableCalories) {
                //   return 0.40 * availableCalories / 4;
                // },
            },
            // {
            //   id: 'test_f10', 
            //   name: '[Test] Low fat (10%)', 
            //   fatFactor: 0.10

            // },
        ];

        function init() {
            vm.storage = $localStorage.$default({
                weightKg: '',
                selectedActivityIndex: 1,
                selectedDeficitIndex: 1,
                selectedMacroSplitIndex: 1,
                inputUnitsWeight: 'kg',
            });

            _selectedActivity = vm.activityOptions[vm.storage.selectedActivityIndex];
            _selectedDeficit = vm.deficitOptions[vm.storage.selectedDeficitIndex];
            _selectedMacroSplit = vm.macroSplitOptions[vm.storage.selectedMacroSplitIndex];

            // INIT: vm.storage.weightKg is always in kg!  
            vm.inputWeight = (vm.storage.inputUnitsWeight === 'kg') ? vm.storage.weightKg : (vm.storage.weightKg * _kgToPoundRatio);
        }

        Object.defineProperty(vm, "selectedActivity", {
            get: function () {
                return _selectedActivity;
            },
            set: function (value) {
                _selectedActivity = value;
                var index = _.indexOf(vm.activityOptions, value);
                vm.storage.selectedActivityIndex = index;
            }
        });

        Object.defineProperty(vm, "selectedDeficit", {
            get: function () {
                return _selectedDeficit;
            },
            set: function (value) {
                _selectedDeficit = value;
                var index = _.indexOf(vm.deficitOptions, value);
                vm.storage.selectedDeficitIndex = index;
            }
        });

        Object.defineProperty(vm, "selectedMacroSplit", {
            get: function () {
                return _selectedMacroSplit;
            },
            set: function (value) {
                _selectedMacroSplit = value;
                var index = _.indexOf(vm.macroSplitOptions, value);
                vm.storage.selectedMacroSplitIndex = index;
            }
        });

        Object.defineProperty(vm, "inputWeight", {
            get: function () {
                return _inputWeight;
            },
            set: function (value) {
                _inputWeight = value;
                vm.storage.weightKg = convertInputWeightToKg(_inputWeight);
            }
        });

        Object.defineProperty(vm, "weightLb", {
            get: function () {
                if (vm.storage.weightKg) {
                    return vm.storage.weightKg * _kgToPoundRatio;
                }
                return '';
            }
        });

        Object.defineProperty(vm, "kinobodyEstimateMaintenanceCalories", {
            get: function () {
                if (vm.weightLb) {
                    return vm.selectedActivity.kinoFactor * vm.weightLb;
                }
                return '';
            }
        });

        Object.defineProperty(vm, "kinobodyEstimateMaintenanceCalories_display", {
            get: function () {
                if (vm.weightLb) {
                    return formatCalNumber(vm.kinobodyEstimateMaintenanceCalories);
                }
                return '';
            }
        });

        Object.defineProperty(vm, "activeMaintenanceFormula", {
            get: function () {
                if (vm.kinobodyEstimateMaintenanceCalories) {
                    return 'KB'; // only KB estimate available -> use KB (good estimate)
                }
                return '';
            }
        });


        Object.defineProperty(vm, "maintenanceCalories", {
            get: function () {
                if (vm.kinobodyEstimateMaintenanceCalories) {
                    return formatCalNumber(vm.kinobodyEstimateMaintenanceCalories);
                }
                return '';
            }
        });

        Object.defineProperty(vm, "deficitCalories", {
            get: function () {
                if (vm.maintenanceCalories) {
                    return formatCalNumber(vm.maintenanceCalories * vm.selectedDeficit.value);
                }
                return '';
            }
        });

        Object.defineProperty(vm, "macrosProtein", {
            get: function () {
                // 2g of protein pr kg / 0.9g per lb
                if (vm.deficitCalories) {
                    var proteinGrams = 0;
                    if (vm.selectedMacroSplit.getProteinGrams) {
                        proteinGrams = vm.selectedMacroSplit.getProteinGrams(vm.storage.weightKg, vm.storage.gender, vm.deficitCalories);
                    } else {
                        proteinGrams = vm.storage.weightKg * vm.selectedDeficit.proteinKgFactor;
                    }
                    return formatCalNumber(proteinGrams);
                }
                return '';
            }
        });

        Object.defineProperty(vm, "macrosFats", {
            get: function () {
                // 25% of calories from fat
                if (vm.deficitCalories) {
                    var fatGrams = 0;
                    if (vm.selectedMacroSplit.getFatGrams) {
                        fatGrams = vm.selectedMacroSplit.getFatGrams(vm.storage.weightKg, vm.storage.gender, vm.deficitCalories);
                    } else {
                        var fatsFactor = vm.selectedMacroSplit.fatFactor;
                        fatGrams = vm.deficitCalories * fatsFactor / 9;
                    }
                    return formatCalNumber(fatGrams);
                }
                return '';
            }
        });

        Object.defineProperty(vm, "macrosCarbs", {
            get: function () {
                // the rest from carbs
                if (vm.deficitCalories) {
                    var carbGrams = 0;
                    if (vm.selectedMacroSplit.getCarbGrams) {
                        carbGrams = vm.selectedMacroSplit.getCarbGrams(vm.storage.weightKg, vm.storage.gender, vm.deficitCalories);
                    } else {
                        var calsProtein = vm.macrosProtein * 4;
                        var calsFats = vm.macrosFats * 9;
                        var calsPF = calsProtein + calsFats;
                        var calsCarbs = vm.deficitCalories - calsPF;
                        carbGrams = calsCarbs / 4;
                    }
                    return formatCalNumber(carbGrams);
                }
                return '';
            }
        });

        Object.defineProperty(vm, "percentageProtein", {
            get: function () {
                if (vm.macrosProtein) {
                    var calsFats = vm.macrosProtein * 4;
                    var p = calsFats / vm.deficitCalories * 100;
                    return formatCalNumber(p);
                }
                return '';
            }
        });

        Object.defineProperty(vm, "percentageFats", {
            get: function () {
                if (vm.macrosFats) {
                    var calsFats = vm.macrosFats * 9;
                    var p = calsFats / vm.deficitCalories * 100;
                    return formatCalNumber(p);
                }
                return '';
            }
        });

        Object.defineProperty(vm, "percentageCarbs", {
            get: function () {
                if (vm.macrosCarbs) {
                    var calsCarbs = vm.macrosCarbs * 4;
                    var p = calsCarbs / vm.deficitCalories * 100;
                    return formatCalNumber(p);
                }
                return '';
            }
        });

        Object.defineProperty(vm, "crossCheckCalories", {
            get: function () {
                if (vm.macrosProtein && vm.macrosFats && vm.macrosCarbs) {
                    var calsProtein = vm.macrosProtein * 4;
                    var calsFats = vm.macrosFats * 9;
                    var calsCarbs = vm.macrosCarbs * 4;
                    return formatCalNumber(calsProtein + calsFats + calsCarbs);
                }
                return '';
            }
        });

        vm.formatCalNumber = formatCalNumber;
        //vm.onActivityChange = onActivityChange;
        //vm.onDeficitChange = onDeficitChange;
        vm.resetStorage = resetStorage;
        vm.toggleInputUnitsWeight = toggleInputUnitsWeight;

        function formatCalNumber(i) {
            if (i === '') return '';
            return i.toFixed(0);
        }

        /*
        function onActivityChange() {
          var index = _.indexOf(vm.activityOptions, vm.selectedActivity);
          vm.storage.selectedActivityIndex = index;
        }
        
        function onDeficitChange() {
          var index = _.indexOf(vm.deficitOptions, vm.selectedDeficit);
          vm.storage.selectedDeficitIndex = index;
        }
        */

        function resetStorage() {
            $localStorage.$reset();
            init();
        }

        function toggleInputUnitsWeight() {
            $log.log('toggleInputUnitsWeight');
            switch (vm.storage.inputUnitsWeight) {
                case 'kg':
                    // LBS
                    vm.storage.inputUnitsWeight = 'lbs';
                    vm.inputWeight = vm.inputWeight * _kgToPoundRatio;
                    break;
                case 'lbs':
                    // KG
                    vm.storage.inputUnitsWeight = 'kg';
                    vm.inputWeight = vm.inputWeight / _kgToPoundRatio;
                    break;
            }
        }

        function convertInputWeightToKg(inputWeight) {
            if (vm.storage.inputUnitsWeight === 'kg') {
                return inputWeight;
            } else {
                return inputWeight / _kgToPoundRatio;
            }
        }

        init();
    }

})();