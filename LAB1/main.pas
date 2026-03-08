program Main;

{$mode objfpc}{$H+}

uses
  Numbers;

const
  COUNT = 50;

var
  Arr: array[0..COUNT - 1] of Integer;
  I: Integer;

begin
  WriteLn('Generating ', COUNT, ' random numbers from 0 to 100:');
  GenerateRandom(Arr);

  for I := 0 to COUNT - 1 do
    Write(Arr[I], ' ');
  WriteLn;
end.
