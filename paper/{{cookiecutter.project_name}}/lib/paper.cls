% ----------------------------------------------------------------------- %
% paper.cls - Paper class based on KOMA scrartcl                          %
% 2012-2015 Abdó Roig-Maranges <abdo.roig@gmail.com>                      %
% ----------------------------------------------------------------------- %

\def\documentclassname{paper}

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{\documentclassname}



% ----------------------------------------------------------------------- %
% Load stuff                                                              %
% ----------------------------------------------------------------------- %

\LoadClassWithOptions{scrartcl}    % load documentclass



% ----------------------------------------------------------------------- %
% Settings                                                                %
% ----------------------------------------------------------------------- %

% Load koma stuff
\RequirePackage{abdokoma}

% geometry
\geometry{left=3cm, right=3cm, top=4cm, bottom=3cm}

% half line separation between paragraphs
\KOMAoptions{parskip=half+}
