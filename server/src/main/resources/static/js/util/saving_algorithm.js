function savings_algorithm(path_number, distances) {
    if (path_number >= distances.length) {
        console.log("최대 가질 수 있는 경로 개수보다 많습니다");
        return;
    }

    // 경로 초기화
    const routes = [...Array(distances.length - 1)].map((_, i) => [0, i + 1, 0]);

    while (true) {
        if (path_number === routes.length) {
            return routes;
        }

        const savings_list = [];
        for (let i = 1; i < routes.length; i++) {
            for (let j = 0; j < routes.length - i; j++) {
                const first = Array.from(new Set([routes[j][1], routes[j][routes[j].length - 2]]));
                const second = Array.from(new Set([routes[j + i][1], routes[j + i][routes[j + i].length - 2]]));

                for (let k = 0; k < first.length; k++) {
                    for (let l = 0; l < second.length; l++) {
                        const sij =
                            distances[first[k]][0] +
                            distances[0][second[l]] -
                            distances[first[k]][second[l]];

                        savings_list.push([sij, j, j + i, first[k], second[l]]);
                    }
                }
            }
        }

        savings_list.sort((a, b) => b[0] - a[0]);

        if (savings_list.length === 0 || savings_list[0][0] <= 0) {
            break;
        }

        const [s, i, j, first, second] = savings_list[0];

        if (routes[i][1] === first) routes[i].reverse();
        if (routes[j][1] !== second) routes[j].reverse();

        routes[i] = routes[i].slice(0, -1).concat(routes[j].slice(1));
        routes.splice(j, 1);
    }

    return routes;
}




