program Main;

{$mode objfpc}{$H+}

uses
  Numbers;

const
  COUNT = 50;
  MIN_VAL = 0;
  MAX_VAL = 100;

var
  Arr: array[0..COUNT - 1] of Integer;
  I: Integer;

begin
  WriteLn('Generating ', COUNT, ' random numbers from ', MIN_VAL, ' to ', MAX_VAL, ':');
  GenerateRandom(Arr, MIN_VAL, MAX_VAL);

  for I := 0 to COUNT - 1 do
    Write(Arr[I], ' ');
  WriteLn;

  WriteLn;
  WriteLn('After sorting:');
  SortNumbers(Arr);

  for I := 0 to COUNT - 1 do
    Write(Arr[I], ' ');
  WriteLn;
end.
